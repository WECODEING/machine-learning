
#include <bits/stdc++.h>

using namespace std;

const int inf=0x3f3f3f3f;


struct node{
	double x,y;
};

vector<node>means[10];//��������� 
vector<node>center;//�������ĵ� 

int K=0,N=0;

double distance(double a,double b,double c,double d)
{
	return sqrt(pow(a-c,2)+pow(b-d,2));//����ŷ�Ͼ��� 
}


bool findcenter(int a)
{
	int s=means[a].size();
	double t1,t2;
	t1=t2=0;
	for(int i=0;i<s;i++)
	{
		t1+=means[a][i].x;
		t2+=means[a][i].y;
	}
	t1/=s;
	t2/=s;
	if(t1==center[a].x && t2==center[a].y)return true;
	else
	{
		center[a].x=t1;
		center[a].y=t2;
		return false;
	}
}

void kmeans(int k)
{
	for(int i=1;i<=k;i++)means[i].clear();
	int flag=1;
	for(int i=0;i<N;i++)//���� 
	{
		double dis=inf;
		int z=0;
		for(int t=1;t<=k;t++)
		{
			double a,b,c,d;
			a=means[0][i].x;
			b=means[0][i].y;
			c=center[t].x;
			d=center[t].y;
			double dis1=distance(a,b,c,d);
			if(dis1<dis)z=t,dis=dis1;//ѡ����������� 
		}
		if(z!=0)means[z].push_back(means[0][i]);
	}
	for(int i=1;i<=k;i++)//����ȷ������ 
	{
		if(!findcenter(i))flag=0;//���ж���ı������������ 
	}
	if(flag==0)kmeans(k);
	
	return;
}


int main()
{
	ifstream infile;
	infile.open("data.txt",ios::in);
	if(!infile){
		cout<<"���ܴ��ļ�"<<endl;
		return 0;
	}
	N=0;
	//���ļ����ж�������
	double a,b;
	while(!infile.eof()){
		infile>>a>>b;
		node q;
		q.x=a;
		q.y=b;
		means[0].push_back(q);
		N++;
	}

	//for(int i=0;i<N;i++)cout<<means[0][i].x<<" "<<means[0][i].y<<endl;
	for(int i=0;i<10;i++)center.push_back(node());
	for(K=2;K<=5;K++)
	{
		for(int i=1;i<=K;i++)//�趨��ʼ���� 
		{
			center[i].x=means[0][i-1].x;
			center[i].y=means[0][i-1].y;
		}

		kmeans(K);
		
		ofstream outfile;
		outfile.open(("kmeans" + to_string(k) + ".txt").c_str(),ios::out);
		
        outfile << K << endl;
        for (int i = 1; i <= K; ++i) {
            outfile << means[i].size()+1 << endl;
            outfile << center[i].x << center[i].y << endl;//�������ĵ� 
            for (int j = 0; j < means[i].size(); ++j) {
                outfile << means[i][j].x << ' ' << means[i][j].y << endl;
            }
        }
		
	} 
}


