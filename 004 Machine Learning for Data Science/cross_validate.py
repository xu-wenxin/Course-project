# 4 cross validation
# 使用k折交叉验证

from sklearn.model_selection import cross_validate

# 方差回归评分函数, https://scikit-learn.org/stable/modules/generated/sklearn.metrics.explained_variance_score.html#sklearn.metrics.explained_variance_score 
# 4.1 knn
knn_result=cross_validate(knn_reg,xs,ys,cv=10,n_jobs=-1,scoring=('explained_variance','r2'))

print('knn time: ',knn_result['fit_time'].mean())
print('knn variance score: ',knn_result['test_explained_variance'].mean())
print('knn r2: ',knn_result['test_r2'].mean(),'\n')

# 4.2 svr
svr_result=cross_validate(svr_reg,xs,ys,cv=10,n_jobs=-1,scoring=('explained_variance','r2'))

print('svr time: ',svr_result['fit_time'].mean())
print('svr variance score: ',svr_result['test_explained_variance'].mean())
print('svr r2: ',svr_result['test_r2'].mean())
