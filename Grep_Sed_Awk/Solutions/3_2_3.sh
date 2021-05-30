awk '{
	if(NR>1)
	{
		sum=$3+$4+$5
		printf("%s %d\n", $1,sum);
	}
	
}' marks.txt