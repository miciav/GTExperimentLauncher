#random_dat.sh
#!/bin/bash 
# 

#################################################################################
## questo file genera un .dat dove i SaaS possono appoggiarsi a tutti gli IaaS ##
#################################################################################

#pulizia
rm model_rand.dat

##########################
### Dimensioni insiemi ###
##########################

IaaS=2 #5 #i
SaaS=100 #10 #s --- meglio se multiplo di IaaS
SperI=100 #numero di saas per iaas
App=100 #30 = k  --- meglio se multiplo di SaaS

#-------------------------------------------
#----------- start script --- do not touch -
#-------------------------------------------


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

#gen S2

echo "SaaS-2set starting..."

echo "set S2:=1" >>model_rand.dat
s2=$SaaS
#echo $s2 #debug

while [ $s2 -ge 2 ]
do 
	#echo "dentro il while"
	#echo $s2 #debug
	echo $s2 >>model_rand.dat
	s2=`expr $s2 - 1`
	#echo $s2 #debug
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

#generazione Is[s]

echo "## ---- Ij[j]" >>model_rand.dat

echo "Ij[j] generation..."
saas=1
iaas=1

#let loop=$SaaS/$IaaS

while [ $saas -le $SaaS ]
do
	let iaas=1
	echo "set Ij[" >>model_rand.dat
	echo $saas"]:=" >>model_rand.dat	
	
		while [ $iaas -le $IaaS ]
		do	
			echo $iaas >>model_rand.dat
			let iaas=`expr $iaas + 1`		
		done
	
	echo ";" >>model_rand.dat
	let saas=`expr $saas + 1`
done


echo "Ij[j] generation done."


#generazione Si[i]

echo "## ---- Si[i]" >>model_rand.dat

echo "Si[i] generation..."

iop=1
#sop=1

while [ $iop -le $IaaS ]
do 
	echo "set Si[" >>model_rand.dat
	echo $iop"]:=" >>model_rand.dat
	
	#let loop=$SaaS/$IaaS
	let r=1
	
	#while [ $r -le $loop ]
	while [	$r -le $SaaS ]
	do
		echo $r >>model_rand.dat
		r=`expr $r + 1`
		#sop=`expr $sop + 1`
	done
	
	echo ";" >>model_rand.dat
	iop=`expr $iop + 1`
done

echo "Si[i] generation done."	


#Concatenzione dei parametri di sistema
echo "Adding system parameters..."
cat sys_params.dat >>model_rand.dat

#File generation model-numberofIaaS-SaaS-App.dat
cp model_rand.dat ./data/model-$IaaS-$SaaS-$App-alliaas.dat 
echo "File model-"$IaaS"-"$SaaS"-"$App"-alliaas.dat generated."