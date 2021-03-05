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
	//检查第col列,匹配到第row行结束 
	//即检查(row,col)位置的方块是否合法 
	int i=1,match=1;
	while(i<=row){
		int cnt = 0;
		while(i<=row && res[i][col]==0) i++;
		while(i<=row && res[i][col]==1) cnt++,i++; // 搜索了一段连续区间 
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
	//按行搜索,当前在考虑第row行第id段 可摆放位置从beg开始 
	//尝试每个连续段所摆放的位置
	//printf("row=%d,id=%d,beg=%d\n",row,id,beg);
	if(row>n){
		bool flag = true;
		for(int i=1;i<=m;i++) flag &= check(row,i);
		if(flag == true) output();//认为找到了一组解
		return ; 
	}
	int tot_left = 0;
	for(int i=id;i<=x[row][0];i++)
		tot_left += x[row][i];
	tot_left+=x[row][0]-id; 
		//至少要tot_left个位置才能放下剩下的所有段
	int i=beg;
	while(i<=m-tot_left+1){
		//枚举放置位置 
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
				 		//在(row,k)这个位置,填或不填 都会产生错误
						//这等价于说 是之前行产生了错误 但尚未识别
						while(j>=0){ res[row][i+j]=0; j--; }
						return ;	
					}
				 	else {fflag=false;break;}
				}
				k++;
				//while循环结束后k停在i+j+1位置
				//当本段未填完时，k是下一个所填位置
				//当本段已填完时，k是空格位置，仍需一次检查 
			}
			if(fflag==false){flag = false;break;}
			//这意味着 在i这个起始点往后填第j格(k=i+j)时出现错误 
			//下一次起点应该为k+1 因为k之前作为起点都必然覆盖到k 
		}
		if(flag==false){ 
			//在填写过程中出现错误 
			while(j>=0){ res[row][i+j]=0; j--; }
		//	printf("\n===\n");
			i++;
		} else {
			if(check(row,i+j)==false) {
			//	printf("check(%d,%d)=false\n",row,i+j);
				while(j>=0){ res[row][i+j]=0; j--; }
				//填写没有错误，但每段之间必要空格，该空格导致错误 
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
