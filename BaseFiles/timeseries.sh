#!/bin/bash
#timeseries.sh

series=timeseries-10min  #source file
#classes=12 # card(A) - coerente con random_dat_shuffle.sh
classes=100
hours=24 ### must be >24 hours. 
#hours=24 #1giorno
#hours=288 #12 giorni
H=6 #slot da 10 min in 1 ora... :D

#campioni=0 #numero campioni
campioni=`expr $hours \* 6`

###floating point --> echo "scale=20; 22 / 7" | bc -l   

echo "Generating .dat file with $series as source..."

#salvo il max campione per la normalizzazione

i=1
max=0 #campione massimo per la normalizzazione.
while [ $i -le $campioni ]
do
	act=`awk -v n=$i 'NR==n {print $2}' $series`
	#echo "actual = $act" #debug
	if [ $act -gt $max ]
	then {
		max=$act
		#echo "new_max = $max" #debug
	}
	fi
	
	i=`expr $i + 1`
done

echo "Maximum sample saved for the normalization ($max req/s)."

echo "# $series - file con shifting in base al fuso orario." >$series.dat

k=1
while [ $k -le $classes ]
do
	
	#ratio * [0.2,400] --- ratio della classe. 
	ratio=`expr $RANDOM % 4000 + 20`
	#echo "ratio=$ratio" #debug. 
	ratio=`echo "scale=1; $ratio / 10" | bc -l`
	#echo "ratio/10=$ratio" #debug.
	
	# Assegnazione del fuso orario. 
	#timezone=`expr $RANDOM % 24`
	rnd=`expr $RANDOM % 100 + 1`
	#echo $rnd #debug.
	
	#us-east
	if [ $rnd -ge 1 ] && [ $rnd -le 14 ];
	then {
		timezone=18
		tzname=US-East
	}
	fi
	
	#us-center
	if [ $rnd -ge 15 ] && [ $rnd -le 25 ];
	then {
		timezone=19
		tzname=US-Central
	}
	fi
	
	#us-west
	if [ $rnd -ge 26 ] && [ $rnd -le 39 ];
	then {
		timezone=20
		tzname=US-West
	}
	fi
	
	#eu-east
	if [ $rnd -ge 40 ] && [ $rnd -le 43 ];
	then {
		timezone=23
		tzname=EU-East
	}
	fi
	
	#eu-center
	if [ $rnd -ge 44 ] && [ $rnd -le 60 ];
	then {
		timezone=0
		tzname=EU-Central
	}
	fi
	
	#eu-west
	if [ $rnd -ge 61 ] && [ $rnd -le 70 ];
	then {
		timezone=1
		tzname=EU-West
	}
	fi	
	
	#asia-east
	if [ $rnd -ge 71 ] && [ $rnd -le 90 ];
	then {
		timezone=7
		tzname=Asia-East
	}
	fi
	
	#asia-center
	if [ $rnd -ge 91 ] && [ $rnd -le 96 ];
	then {
		timezone=8
		tzname=Asia-Central
	}
	fi
	
	#asia-west
	if [ $rnd -ge 97 ] && [ $rnd -le 97 ];
	then {
		timezone=9
		tzname=Asia-West
	}
	fi
	
	#oceania
	if [ $rnd -ge 98 ] && [ $rnd -le 100 ];
	then {
		timezone=10
		tzname=Oceania
	}
	fi
	
	echo "Generating $k class... timezone = $tzname with ratio $ratio."
	
	i=1 #rinizio i campioni per la classe. 
	
	tm=`expr $hours - $timezone`
	t=$tm
	
	# da (24-timezone) --> 24
	while [ $t -le $hours ]
	do
		echo "let Lambda[$k,$t]:= " >>$series.dat

		h=1
		x=0
			while [ $h -le $H ]
			do
				temp=`awk -v n=$i 'NR==n {print $2}' $series` #>>$series.dat
				x=`expr $x + $temp`
				h=`expr $h + 1`
				i=`expr $i + 1`
			done

		avg=`expr $x / 6` # slot di 10min in un ora = 6.

		#normalizzo
		#echo "original=$avg" #debug
		avg=`echo "scale=5; $avg / $max" | bc -l `
		#echo "normaliz=$avg" #debug
		
		#ratio
		avg=`echo "scale=5; $avg * $ratio" | bc -l `
		#echo "avg_norm=$avg" #debug
	
		#noise * [0.9,1.1] --- ratio della classe. 
		noise=`expr $RANDOM % 21 + 90`
		#echo "noise=$noise" #debug. 
		noise=`echo "scale=5; $noise / 100" | bc -l `
		#echo "noise_norm=$noise" #debug.
		avg=`echo "scale=5; $avg * $noise" | bc -l `
		#echo "avg_con_noise=$avg" #debug
		#echo "===" #debug
		
		
		echo "$avg ;" >>$series.dat
		t=`expr $t + 1`
	done 
	
	t=1
	tm=`expr $tm - 1`
	
	while [ $t -le $tm ]
	do
		echo "let Lambda[$k,$t]:= " >>$series.dat

		h=1
		x=0
			while [ $h -le $H ]
			do
				temp=`awk -v n=$i 'NR==n {print $2}' $series` #>>$series.dat
				x=`expr $x + $temp`
				h=`expr $h + 1`
				i=`expr $i + 1`
			done

		avg=`expr $x / 6` # slot di 10min in un ora = 6.

		#normalizzo 
		#echo "original=$avg" #debug
		avg=`echo "scale=5; $avg / $max" | bc -l `
		#echo "normaliz=$avg" #debug
		
		#ratio
		avg=`echo "scale=5; $avg * $ratio" | bc -l `
		#echo "avg_norm=$avg" #debug
	
		#noise * [0.9,1.1] --- ratio della classe. 
		noise=`expr $RANDOM % 21 + 90`
		#echo "noise=$noise" #debug. 
		noise=`echo "scale=5; $rnd / 100" | bc -l `
		#echo "noise_norm=$noise" #debug.
		avg=`echo "scale=5; $avg * $noise" | bc -l `
		#echo "avg_con_noise=$avg" #debug
		#echo "===" #debug
		
		echo "$avg ;" >>$series.dat
		t=`expr $t + 1`
	done 

	k=`expr $k + 1`
done

# disattivare -ratio se non lo si vuole. 
#mv $series.dat timeseries-$classes-k-$hours-h.dat
mv $series.dat timeseries-$classes-k-$hours-h-shift.dat

echo "Done."

# disattivare -ratio se non lo si vuole. 
#echo "Use timeseries-$classes-k-$hours-h.dat for AMPL."
echo "Use timeseries-$classes-k-$hours-h-shift.dat for AMPL."


