import numpy as np

#Server Resource Algorithm

# we can like hardcode cnn model
Fi=[20, 30, 40, 50]# flops required per layer
Oi=[100, 80, 50, 20]#output size after each layer
Li=len(Fi) - 1 #total number of layers in the CNN model of user/device i


#say device parameters be:
fl_i=20 #local computation power
pi_tx=2 #transmission power
hi=10 #channel coefficient
sigma2_i=1 #noise power
Ic=1 #interference

deadline = 10

#the ED compute: partition point di, total delay, wheater deadline satisfies
def user_response(wi, fi_edge):
    best_partition = -1
    best_delay = float('inf') #infinity
    best_rl = 0
    best_ru = 0

    #we will try every partition layer and then
    for di in range(Li + 1):
        # local computation FLOPS
        T1 = sum(Fi[:di + 1]) #eqn (5)

        # edge computation FLOPS
        T2 = sum(Fi[di + 1:]) #eqn (6)

        # local inference delay
        rl = T1 / fl_i

        # edge inference delay
        if fi_edge == 0:
            re = float('inf')
        else:
            re = T2 / fi_edge

        # transmission rate
        rate = wi * np.log2(
            1 + (pi_tx * hi) / (sigma2_i + Ic)
        )

        # upload delay
        if rate == 0:
            ru = float('inf')
        else:
            ru = Oi[di] / rate #eqn (7)

        # total collaborative delay
        total_delay = rl + re + ru

        # check deadline
        if total_delay <= deadline:

            # choose best partition
            if total_delay < best_delay:
                best_delay = total_delay
                best_partition = di
                best_rl = rl
                best_ru = ru

    return best_partition, best_delay, best_rl, best_ru

def do_computation(Nx0, W, F):
    Wi_list=[]
    Fi_list=[]
    UxNx0=0
    deadline=10 #max allowed delay or latency

    for i in range(Nx0):
        wi_final=0;fi_final=0;pyi_max=float('-inf')

        #wee will generate ratios
        g=0.1 #can take anything even small as well
        ratios=np.arange(g,0.6,g) #[0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1. ]

        #generate tensor grid
        w_values=ratios*W
        f_values=ratios*F

        #sare combination try karenge
        for w_i in w_values:
            for f_i in f_values:

                if w_i >= W:
                    continue

                if f_i >= F:
                    continue

                if W <= 0 or F <= 0:
                    break

                #compute delay kitna hai
                d_i, delay, rl, ru = user_response(w_i, f_i)

                #deadline constraint check karenge in this
                if d_i != -1:

                    #Compute utility/profit π_i
                    #C_i_0 = Local inference cost
                    #k_i=energy consumption parameter
                    #gamma_i=the unit local energy cost
                    #p_i=the resources allocated to Edi
                    #f_i=Local resources of EDi
                    #beta_i=transmission power efficiency parameter
                    #C_i_0 = 100
                    k_i = 0.5
                    gamma_i = 1.2
                    p_i = 2
                    beta_i = 0.8

                    local_delay = sum(Fi) / fl_i #eqn (2)

                    C_i_0 = (  #eqn (8)
                            local_delay
                            * (fl_i ** 2)
                            * k_i
                            * gamma_i
                    )

                    pi_i = (
                            C_i_0
                            - rl * ((fl_i ** 2) * k_i * gamma_i)
                            - ru * (p_i * beta_i * gamma_i)
                    )

                    # Maximize π_i
                    if pi_i > pyi_max:
                        pyi_max = pi_i
                        wi_final = w_i
                        fi_final = f_i


        #we will store best value
        Wi_list.append(wi_final)
        Fi_list.append(fi_final)

        #and update the remaining resources
        W -= wi_final
        F -= fi_final

        #and update utility
        UxNx0+=pyi_max

    return UxNx0,Wi_list,Fi_list


# def SRA():
#     print("SRA")

#     #input lenge=offloading devices(Nx0),
#     # total bandwidth(W), total computation(F)
#     Nx0=int(input("enter no. of offloading devices: "))
#     W=float(input("enter total bandwidth: "))
#     F=float(input("enter total computation: "))

#     print(Nx0,W,F)

#     #expected output
#     #The utility(UxNx0), bandwidth allocation(Wi_list), computation allocation(Fi_list)
#     return do_computation(Nx0,W, F)

def SRA(i,W,F):
    print("SRA")

    print(i,W,F)

    #expected output
    #The utility(UxNx0), bandwidth allocation(Wi_list), computation allocation(Fi_list)
    return do_computation(i,W, F)


if __name__ == '__main__':
    UxNx0, Wi_list,Fi_list=SRA()
    print(UxNx0)
    print(*Wi_list)
    print(*Fi_list)