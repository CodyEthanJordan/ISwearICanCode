// Varg.c
// 1/22/17
// COP 3502H-0202
// Joshua Pollock

#include "Varg.h"
#include <stdarg.h>

// This checks to see if any characters are more common than the current most frequent and, if so, returns them.
char mostCommonSoFar(int frequency[26], char current)
{

	int i;	
	
	for (i=0; i<26; i++)
	{
		if (frequency[i]>frequency[current-'a'])
			current=i+'a';
	}
	
	return current;

}

// This fuction fills the empty initial frequency array with zeros.
void fillWithZero(int *frequency)
{

	int i;

	for (i=0; i<26; i++)
		frequency[i]=0;

}

// This function accepts a positive integer, then that many lower case characters a-z. It then returns the most common character in that list.
char mostFrequentChar(int first, ...)
{

	char mostFrequent='\0', c;
	int frequency[26], i;
	
	va_list argc;
	
	va_start(argc, first);
	
	fillWithZero(frequency);
	
	for (i=0; i<first; i++)
	{
		c=va_arg(argc, int);
		
		frequency[c-'a']++;
		
		if (mostFrequent=='\0')
			mostFrequent=c;
		else
			mostFrequent=mostCommonSoFar(frequency, mostFrequent);
			
	}
	
	va_end(argc);
		
	return mostFrequent;
}

// This function accepts a list of lower case characters a-z ended with '\0' and returns the most common character.
char fancyMostFrequentChar(char first, ...)
{
	
	char mostFrequent=first, c;
	int frequency[26];
	
	va_list argc;
	
	va_start(argc, first);
	
	fillWithZero(frequency);
	
	if (mostFrequent!='\0')
	{
		frequency[first-'a']++;
		while ((c=va_arg(argc, int))!=0)
		{
			
			frequency[c-'a']++;
			
			mostFrequent=mostCommonSoFar(frequency, mostFrequent);
			
		}
	}
	
	va_end(argc);
		
	return mostFrequent;
	
}

double difficultyRating(void)
{

	return 2.5;

}

double hoursSpent(void)
{

	return 3.0;

}

