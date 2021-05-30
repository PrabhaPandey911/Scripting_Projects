awk '{
if(NR>1)
	{
		if($2=="M")
 			print $0 > "males.txt"
		else if($2=="F")
			print $0 > "females.txt"
	}
 

}' marks.txt