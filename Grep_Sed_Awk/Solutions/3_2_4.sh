awk '
BEGIN{n=0}
{
	if(NR>1)
		{
			n++
			sum[NR-2]=$3+$4+$5
			name[NR-2]=$1
		}
}
END{
	max=sum[0];
	for(i=0;i<n-1;i++)
	{
		if(max<sum[i])
			{
				nm=name[i];
				max=sum[i];
			}
	}
	printf("Topper: \n%s\n",nm);
	for(i=0;i<n-1;i++)
	{
		s=s+sum[i];
	}
	printf("Students above average:\n")
	avg=s/(n-1);
	for(i=0;i<n-1;i++)
	{
		if(sum[i]>avg)
			printf("%s\n",name[i]);
	}
}' marks.txt