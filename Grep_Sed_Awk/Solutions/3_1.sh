awk 'BEGIN{n=0}{n++
array[NR-1]=$0

}END{
	x=0
	for(i=0;i<n;i++)
	{
		f=0;
		for(j=i+1;j<n;j++)
		{
			if(array[i]==array[j])
				{
					f=1;
					break;
				}		
		}
		if(f==0)
			{
				flag[x]=array[i];
				x++;
			}
		
	}
	for(i=0;i<x;i++)
	{
		print flag[i];
	}
}' sample.txt