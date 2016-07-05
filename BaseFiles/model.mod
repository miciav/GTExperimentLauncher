# Generalized Nash Equilibria? for Cloud Federation
# First model - first_model.mod file

# Variables

# --SaaS Decision Variables

var r{k in A, i in I}; # number of reserved VMs used for application k at IaaS site i
#var r{k in A, i in I}, integer; # number of reserved VMs used for application k at IaaS site i

var d{k in A, i in I}; # number of on demand VMs used for application k at IaaS site i
#var d{k in A, i in I}, integer; # number of on demand VMs used for application k at IaaS site i

var s{k in A, i in I}; # number of on spot VMs used for application k at IaaS site i
#var s{k in A, i in I}, integer; # number of on spot VMs used for application k at IaaS site i

var x{k in A, i in I}; # workflow served

# Constraints

# --SaaS constraints

#1
s.t. r_pos{j in S, k in Aj[j], i in I}: r[k,i] >= 0; # number of reserved VMs >= 0
s.t. d_pos{j in S, k in Aj[j], i in I}: d[k,i] >= 0; # number of on demand VMs >= 0
s.t. s_pos{j in S, k in Aj[j], i in I}: s[k,i] >= 0; # number of on spot VMs >= 0
s.t. x_pos{j in S, k in Aj[j], i in I}: x[k,i] >= 0; # workload served >=0

#2
s.t. s_max {j in  S, k in Aj[j],  i in Ij[j]}: s[k,i] <= ( (eta[j]/(1-eta[j]))*(r[k,i]+d[k,i]) ); # number of on spot VMs less than fixed ration of on demand VMs 

#3
s.t. X_min {j in S, k in Aj[j]} : sum{i in Ij[j]} ( (mu[k,i] - 1 / (overlineR[k] - D[k,i]) )*( r[k,i]+d[k,i]+s[k,i] ) ) >= lambdaCurrent[k]; # X lowerbound

s.t. X_max {j in S, k in Aj[j]} : sum{i in Ij[j]} ( (mu[k,i] - 1 / (overlineR[k] - D[k,i]) )*( r[k,i]+d[k,i]+s[k,i] ) ) <= LambdaCurrent[k]; # X upperbound

#4
s.t. R_max {j in S, i in Ij[j]}: sum{k in Aj[j]} (r[k,i]) <= R[j,i]; # on demand VMs upperbound

#5
s.t. vm_max{j in S, i in Ij[j]}: sum{y in Si[i], k in Aj[y]} (r[k,i] + d[k,i] + s[k,i]) <= N[i]; # upperbound of VMs that can be executed at IaaS site i

#5mauro con check sul flag

s.t. vm_max_mauro{j in S, i in Ij[j]: flag[j,i]=1 }: sum{k in Aj[j]} (r[k,i] + d[k,i] + s[k,i]) = N_alg2[j,i];

#s.t. vm_max_unflag{j in S, i in Ij[j]: flag[j,i]=0 }: sum{y in Si[i], k in Aj[y]} (r[k,i] + d[k,i] + s[k,i]) <= N[i]; 

#5threshold this constraint is used only in the utilization-based threshold model

s.t. U_threshold{j in S, k in Aj[j], i in Ij[j] }: x[k,i]/U - ( r[k,i]+d[k,i]+s[k,i])*mu[k,i] <=0;

#3threshold override the version that dopped the x[k,i]
s.t. X_min_threshold {j in S, k in Aj[j]} : sum{i in Ij[j]} ( x[k,i] ) >= lambdaCurrent[k]; # X lowerbound
s.t. X_max_threshold {j in S, k in Aj[j]} : sum{i in Ij[j]} ( x[k,i] ) <= LambdaCurrent[k]; # X upperbound

# Objective functions 

# --SaaS problem

minimize omegaj{j in S}: 
	sum{k in Aj[j]}(
		Time*nu[k]*LambdaCurrent[k]
		+
		sum{i in Ij[j]}(
			rhoCurrent[i]*r[k,i] +
			deltaCurrent[i]*d[k,i] + 
			sigmamaxCurrent[j,i]*s[k,i] - 
			Time*nu[k]*( mu[k,i] - (1 / (overlineR[k]-D[k,i])) )*(r[k,i]+d[k,i]+s[k,i])
		) 	
	)
;

# --SaaS problem threshold version
minimize omegaj_threshold{j in S}: 
	sum{k in Aj[j]}(
		Time*nu[k]*LambdaCurrent[k]
		+
		sum{i in Ij[j]}(
			rhoCurrent[i]*r[k,i] +
			deltaCurrent[i]*d[k,i] + 
			sigmamaxCurrent[j,i]*s[k,i] - 
			Time*nu[k]*( x[k,i])
		) 	
	)
;



