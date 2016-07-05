# Generalized Nash Equilibria? for Cloud Federation
# First model - potential.mod file

# potential function

minimize potential: 
	sum{j in S}(
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
	)
;