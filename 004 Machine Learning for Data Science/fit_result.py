def score(algorithm, ys_train, ys_train_pred,ys_test, ys_test_pred):
    # Variance
    from sklearn.metrics import explained_variance_score
    print('Train score of',algorithm,' train set', explained_variance_score(ys_train, ys_train_pred))
    print('Test score of',algorithm,' test set', explained_variance_score(ys_test, ys_test_pred),'\n')

    # Mean value of the fitting error
    from sklearn.metrics import mean_absolute_error
    print('Train mean error of',algorithm,' train set', mean_absolute_error(ys_train, ys_train_pred))
    print('Test mean error of',algorithm,' test set', mean_absolute_error(ys_test, ys_test_pred),'\n')

    # r2
    from sklearn.metrics import r2_score
    print('Train R2 of',algorithm,' train set', r2_score(ys_train, ys_train_pred))
    print('Test R2 score of',algorithm,' test set', r2_score(ys_test, ys_test_pred))
