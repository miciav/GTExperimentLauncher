#random_dat.sh
#!/bin/bash 
# 

#########################################################################################
## questo file genera un .dat dove i SaaS possono appoggiarsi a N (non tutti) gli IaaS ##
#########################################################################################

#pulizia
rm model_rand.dat

##########################
### Dimensioni insiemi ###
##########################

IaaS=10 #10 # card(I)
SaaS=100 #20 #s card(S)
IperS=3 #3 #numero di iaas per saas --- strettamente minore di iaas -- per assegnarli tutti c'è random_dat_alliaas.sh
App=100 #120 # card(A)  --- meglio se multiplo di SaaS


#-------------------------------------------
#----------- start script --- do not touch -
#-------------------------------------------

#SHUFFLE for S2
#This function shuffles the elements of an array in-place using the Knuth-Fisher-Yates shuffle algorithm.

#init dell'array
s=0
while [ $s -lt $SaaS ]
do
	array[$s]=`expr $s + 1`
	s=`expr $s + 1`
done

#shuffle function
shuffle() {
   local i tmp size max rand

   # $RANDOM % (i+1) is biased because of the limited range of $RANDOM
   # Compensate by using a range which is a multiple of the array size.
   size=${#array[*]}
   max=$(( 32768 / size * size ))

   for ((i=size-1; i>0; i--)); do
      while (( (rand=$RANDOM) >= max )); do :; done
      rand=$(( rand % (i+1) ))
      tmp=${array[i]} array[i]=${array[rand]} array[rand]=$tmp
   done
}

#shuffle array
shuffle

#inizio generazione sets
echo "# -- Sets" >model_rand.dat

#generazione set IaaS
echo "IaaS starting..."

echo "set I:=1" >>model_rand.dat
i=2

while [ $i -le $IaaS ]
do 
	echo $i >>model_rand.dat
	i=`expr $i + 1`
done
echo ";" >>model_rand.dat

echo "IaaS done."

#generazione set SaaS - 1...N
echo "SaaS-1set starting..."

echo "set S:=1" >>model_rand.dat
s=2

while [ $s -le $SaaS ]
do 
	echo $s >>model_rand.dat
	s=`expr $s + 1`
done
echo ";" >>model_rand.dat

echo "SaaS-1set done."

#generazione set SaaS2 - random

echo "SaaS-2set starting..."

echo "set S2:=" >>model_rand.dat

s2=0

while [ $s2 -le $SaaS ]
do
	echo ${array[$s2]}>>model_rand.dat
	s2=`expr $s2 + 1`
done

echo ";" >>model_rand.dat

echo "SaaS-2set done."


#generazione set App
echo "App starting..."

echo "set A:=1" >>model_rand.dat
a=2

while [ $a -le $App ]
do 
	echo $a >>model_rand.dat
	a=`expr $a + 1`
done
echo ";" >>model_rand.dat

echo "App done."

# Associazioni

echo "# -- Associations" >>model_rand.dat

#generazione As[s]

echo "## ---- Aj[j]" >>model_rand.dat

echo "Aj[j] generation..."
aats=1
app=1
#echo "aats=" $aats "app=" $app

while [ $aats -le $SaaS ]
do 
	echo "set Aj[" >>model_rand.dat
	echo $aats"]:=" >>model_rand.dat
	
	k=1
#	echo "k= " $k
	
	let loop=$App/$SaaS
#	echo "Number of App for each SaaS = " $loop
	
	while [ $k -le $loop ]
	do
		echo $app >>model_rand.dat
		app=`expr $app + 1`
		k=`expr $k + 1`
	done
	echo ";" >>model_rand.dat	
	aats=`expr $aats + 1`
done

echo "Aj[j] generation done."

#generazione Sa[s] <<< rimossa perchè 1 app può essere hostata solo da 1 SaaS

#echo "## ---- Sa[a]" >>model_rand.dat

#echo "Sa[a] generation..."
#sata=1
#saas=1

#while [ $sata -le $App ]
#do 
#	echo "set Sa[" >>model_rand.dat
#	echo $sata"]:=" >>model_rand.dat
#	
#	let loop=$App/$SaaS
#	let temp=$sata%$loop	
#		
#	if [ $temp -eq 0 ];
#		then let temp=$sata/$loop
#		else let temp=$sata/$loop+1
#	fi	
		
	#let temp=$sata/$loop
	#let temp=temp+1
	
#	echo $temp >>model_rand.dat
#	echo ";" >>model_rand.dat
#	
#	sata=`expr $sata + 1`
#done

#echo "Sa[a] generation done."

#Mancano la generazione di Is[s] e Si[i]

#generazione Ij[j]

echo "## ---- Ij[j]" >>model_rand.dat

echo "Ij[j] generation..."
saas=1
i=1
incr=0
temp=0
#let loop=$SaaS/$IaaS

while [ $saas -le $SaaS ]
do
	temp=`expr $saas % $IaaS`
	let i=1
	echo "set Ij[" >>model_rand.dat
	echo $saas"]:=" >>model_rand.dat	
	
	while [ $i -le $IperS ]
	do
		if [ $temp -eq 0 ]
		then
			echo $IaaS>>model_rand.dat
		elif [ $temp -gt $IaaS ]
		then
			echo `expr $temp - $IaaS`>>model_rand.dat
		else
			echo $temp>>model_rand.dat
		fi
		i=`expr $i + 1`
		temp=`expr $temp + 1`
	done
	
	echo ";">>model_rand.dat	
	
	saas=`expr $saas + 1`
done

echo "Ij[j] generation done."


#generazione Si[i]

#echo "## ---- Si[i]" >>model_rand.dat

#echo "Si[i] generation..."

#iaas=1
#cosi si ottiene il valore assoluto
#abs_value=-1234; echo ${abs_value#-}

#while [ $iaas -le $IaaS ]
#do
#	echo "set Si[" >>model_rand.dat
#	echo $iaas"]:=" >>model_rand.dat
#	
#	s=1

#	check1=`expr $iaas - $IperS + 1`	
	#if [ $first -eq 0 ] && [ $second -eq 0 ]
	
	
#	while [ $s -le $SaaS ]
#	do	
#		check2=`expr $s % $IaaS` ## check modulo
		#echo $check2
#		check3=`expr $IaaS - $iaas`
		#echo $check3
		
#		if [ $check1 -lt 0 ] 
#		then 
#			if [ $check2 -le $iaas ]
#			then echo $s>>model_rand.dat
#			else
#				if [ $check2 -eq $check3 ]
#				then echo $s>>model_rand.dat
#				fi
#			fi	
#		else
#			if [ $iaas -eq $IaaS ]
#			then
#				if [ `expr $check1 - 1` -le $check2 ] && [ $check2 -le $iaas ] 
#				then
#				echo `expr $s + 1` >>model_rand.dat
#				fi
#			else
#				if [ $check1 -le $check2 ] && [ $check2 -le $iaas ]
#				then
#				echo $s>>model_rand.dat
#				fi
#			fi
#		fi
#			
#	s=`expr $s + 1`
#	done
#	
#	echo ";">>model_rand.dat
#	iaas=`expr $iaas + 1`
#done


#echo "Si[i] generation done."	


#Concatenzione dei parametri di sistema
echo "Adding system parameters..."
cat sys_params.dat >>model_rand.dat

#File generation model-#IaaS-#SaaS-#App.dat
cp model_rand.dat ./data/model-$IaaS-i-$SaaS-j-$App-k-$IperS-ixj-shuffle.dat 
echo "File model-"$IaaS"-i-"$SaaS"-j-"$App"-k-"$IperS"-ixj-shuffle.dat generated."