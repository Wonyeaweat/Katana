#include <iostream>
#include <fstream>
#include <cstdio>
using namespace std;
int n, m;
int x[200][200], y[200][200];
int res[200][200]={0};
void init(){
    scanf("%d %d", &n, &m);
    for (int i = 1; i <= n; i++){
        scanf("%d", &x[i][0]);
        for (int j = 1; j <= x[i][0]; j++)
			scanf("%d", &x[i][j]);
    }
    for (int i = 1; i <= m; i++){
        scanf("%d", &y[i][0]);
        for (int j = 1; j <= y[i][0]; j++)
            scanf("%d", &y[i][j]);
    }
}

bool check(int row,int col){
	//����col��,ƥ�䵽��row�н��� 
	//�����(row,col)λ�õķ����Ƿ�Ϸ� 
	int i=1,match=1;
	while(i<=row){
		int cnt = 0;
		while(i<=row && res[i][col]==0) i++;
		while(i<=row && res[i][col]==1) cnt++,i++; // ������һ���������� 
		if(cnt>0 && match>y[col][0]) return false;
		if(i>row){
			if(cnt>y[col][match]) return false;
			return true;
		} else {
			if(cnt!=y[col][match]) return false;
			else match++;
		}
	}
	return true;
}

void output(){
	//printf("%d %d\n",n,m);
	for(int i=1;i<=n;i++){
		for(int j=1;j<=m;j++){
			printf("%d ",res[i][j]);
			//if(j%5==0) printf(" ");
		}
		//if(i%5==0) printf("\n");
		printf("\n");
	}
	printf("\n");
}


void dfs(int row,int id,int beg){
	//��������,��ǰ�ڿ��ǵ�row�е�id�� �ɰڷ�λ�ô�beg��ʼ 
	//����ÿ�����������ڷŵ�λ��
	//printf("row=%d,id=%d,beg=%d\n",row,id,beg);
	if(row>n){
		bool flag = true;
		for(int i=1;i<=m;i++) flag &= check(row,i);
		if(flag == true) output();//��Ϊ�ҵ���һ���
		return ; 
	}
	int tot_left = 0;
	for(int i=id;i<=x[row][0];i++)
		tot_left += x[row][i];
	tot_left+=x[row][0]-id; 
		//����Ҫtot_left��λ�ò��ܷ���ʣ�µ����ж�
	int i=beg;
	while(i<=m-tot_left+1){
		//ö�ٷ���λ�� 
		int j=0,next;
		bool flag=true;
		int k=beg;
		for(;j<x[row][id];j++){
			res[row][i+j]=1;
			bool fflag=true;
	     //   if(row==5)output();
			while(k<=i+j && k<=m){
				if(check(row,k)==false){
		//			printf("check(%d,%d)=false\n",row,k);
				 	if(k<i) {
				 		//��(row,k)���λ��,����� �����������
						//��ȼ���˵ ��֮ǰ�в����˴��� ����δʶ��
						while(j>=0){ res[row][i+j]=0; j--; }
						return ;	
					}
				 	else {fflag=false;break;}
				}
				k++;
				//whileѭ��������kͣ��i+j+1λ��
				//������δ����ʱ��k����һ������λ��
				//������������ʱ��k�ǿո�λ�ã�����һ�μ�� 
			}
			if(fflag==false){flag = false;break;}
			//����ζ�� ��i�����ʼ���������j��(k=i+j)ʱ���ִ��� 
			//��һ�����Ӧ��Ϊk+1 ��Ϊk֮ǰ��Ϊ��㶼��Ȼ���ǵ�k 
		}
		if(flag==false){ 
			//����д�����г��ִ��� 
			while(j>=0){ res[row][i+j]=0; j--; }
		//	printf("\n===\n");
			i++;
		} else {
			if(check(row,i+j)==false) {
			//	printf("check(%d,%d)=false\n",row,i+j);
				while(j>=0){ res[row][i+j]=0; j--; }
				//��дû�д��󣬵�ÿ��֮���Ҫ�ո񣬸ÿո��´��� 
				i++;
			} else {
				if(id >= x[row][0]) dfs(row+1,1,1);
				else dfs(row,id+1,i+j+1);
				while(j>=0){ res[row][i+j]=0; j--; }
				i++;	
			}
		}
	} 
}

int main(){
	freopen("./Analyze/data.dat", "r", stdin);
	freopen("./Analyze/result.dat","w",stdout);
	init();
	dfs(1,1,1);
    return 0;
}
