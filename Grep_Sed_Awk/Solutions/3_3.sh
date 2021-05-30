awk 'BEGIN{print "["}
{
	if(FNR==NR)
		{
			last++;next
		}
	if(last!=FNR)
		{
			printf("\t{");
			printf("\n\t\"ID\" : \"%s\" ,",substr($1,1,length($1)-1));
			i=2
			b=""
			while(i<(NF-1))
			{
				b=b" "$i;
				i++;
			}
			printf("\n\t\"Name\" : \"%s \" ,",b);
			printf("\n\t\" Year \" : \" %s \" ,", substr($(NF-1),2,(length($(NF-1))-2)));
			printf("\n\t\" Rating \" : \" %s \" ", $NF);
			printf("\n\t} ,\n");
		}
	else{
		printf("\t{");
		printf("\n\t\"ID\" : \"%s\" ,",substr($1,1,length($1)-1));
		i=2
		b=""
		while(i<(NF-1))
		{
			b=b" "$i;
			i++;
		}
		printf("\n\t\"Name\" : \"%s \" ,",b);
		printf("\n\t\" Year \" : \" %s \" ,", substr($(NF-1),2,(length($(NF-1))-2)));
		printf("\n\t\" Rating \" : \" %s \" ", $NF);
		printf("\n\t} ");
	}
}
END{printf("\n]\n");}' imdb-top-250.txt imdb-top-250.txt 