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
	for(i=0;i<n;i++)
	{
		if(sum[i]>=95 && sum[i]<=100)
			{
				printf("%s %s\n",name[i],A);
			}
		else if(sum[i]>=90 && sum[i]<95)
			{
				printf("%s A-\n",name[i]);
			}
		else if(sum[i]>=85 && sum[i]<90)
			{
				printf("%s B\n",name[i]);
			}
		else if(sum[i]>=80 && sum[i]<85)
			{
				printf("%s B-\n",name[i]);
			}
		else if(sum[i]>=75 && sum[i]<80)
			{
				printf("%s C\n",name[i]);
			}
		else if(sum[i]>=70 && sum[i]<75)
			{
				printf("%s C-\n",name[i]);
			}
		else if(sum[i]>=60 && sum[i]<70)
		{
			printf("%s D\n",name[i]);
		}
		else if(sum[i]<60)
		{
			printf("%s F\n",name[i]);
		}
	}
}' marks.txt