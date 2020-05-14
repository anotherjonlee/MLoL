def plot_cm(ax, estimator, X_test, y_test):
     
    """
    input:  a plt.subplot object, an estimator object, X_test array, y_test array
    output: a confusion matrix plot
    """
    
    from sklearn.metrics import plot_confusion_matrix
    import matplotlib.pyplot as plt
    import seaborn as sns
    plt.style.use('ggplot')

    ax = plot_confusion_matrix(classifier, X_test, y_test,
                                display_labels=class_names,
                                cmap=plt.cm.Blues,
                                normalize=normalize)
    plt.show()
    
def general_correlation_plot(df):
    
    """
    input:  a plt.subplot object and a pandas dataframe
    output: a correlation plot 
    """
    
    import matplotlib.pyplot as plt
    import seaborn as sns
    plt.style.use('ggplot')
    
    hue = {'red':'red','blue':'blue'}
    
    sns.pairplot(df,corner = True,hue = hue)
    plt.show()
    
def granular_correlation_plot(ax,df, var1, var2, var3 = None):
    
    """
    input:  a plt.subplot object, a pandas dataframe, feature names (string)
    output: a correlation plot 
    """
    
    import matplotlib.pyplot as plt
    import seaborn as sns
    plt.style.use('ggplot')
    
    if var3 == None:
        ax = sns.pairplot(df,
                        corner = True,
                        hue = 'teams',
                        vars=[var1, var2])
        plt.show()
    
    else:
        ax = sns.pairplot(df,
                        corner = True,
                        hue = 'teams',
                        vars=[var1, var2, var3])
        plt.show()
        
def box_plot(ax, df, x, y, hue_var = None):
    """
    input:matplotlib object(ax), dataframe, x(array),y(array),hue_var(array)
    output:box plot
    """
    
    import matplotlib.pyplot as plt
    import seaborn as sns
    plt.style.use('ggplot')
    
    if hue_var == None:
        ax = sns.boxplot(x = x,  
                         data = df,
                         orient = 'h')
    else:
        ax = sns.boxplot(x = x, 
                         data = df,
                         hues = hue_var,
                         orient = 'h')
    plt.show()
    
def roc_auc_plot(ax, estimator, df_test, X_test, y_test):
    import matplotlib.pyplot as plt
    import seaborn as sns
    plt.style.use('ggplot')
    from sklearn.metrics import RocCurveDisplay, auc, roc, roc_curve
    
    y_score = estimator.decision_function(X_test)

    fpr, tpr, _ = roc_curve(y_test, y_score, pos_label=estimator.classes_[1])
    #ax = RocCurveDisplay(fpr=fpr, tpr=tpr).plot()
    
    fpr, tpr, thresholds = metrics.roc_curve(y, pred)
    
    roc_auc = metrics.auc(fpr, tpr)
    
    ax = metrics.RocCurveDisplay(fpr=fpr, tpr=tpr, 
                                      roc_auc=roc_auc, 
                                      estimator_name='example estimator')
    """ax.plot(fpr, 
            tpr, 
            color='darkred',
            lw=lw, 
            label='ROC curve (area = %0.2f)' % roc_auc_rf)"""
    
    ax.plot([0, 1], [0, 1], 
             color='navy', 
             lw=lw, 
             linestyle='--')
    
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    
    plt.title('ROC-AUC')
    plt.legend(bbox_to_anchor=(1.05,1),loc=2,borderaxespad=0)
    #plt.legend(loc="lower right")
    plt.show()
    