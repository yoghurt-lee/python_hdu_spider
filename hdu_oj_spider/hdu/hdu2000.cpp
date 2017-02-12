#include <iostream>
using namespace std;
void sortChar(char a[],int n)
{
	for (int i = 0;i < n; i++)
		for (int j = i+1; j < n; j++) 
		{
			if(a[i] > a[j])
			{
				char temp = a[i];
				a[i] = a[j];
				a[j] = temp;
			}
 		}
}
int main()
{
	char a[3];
	while(cin>>a)
	{
		sortChar(a,strlen(a));
		for (int j = 0; j < strlen(a); j++) {
			cout<<a[j];
			if(j != strlen(a)-1)
				cout<<" ";
		}
		cout<<endl;
	}
	return 0;
}