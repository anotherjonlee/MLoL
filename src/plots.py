def plot_cm(ax, estimator, X_test, y_test):
     
    """
    input:  a plt.subplot object, an estimator object, X_test array, y_test array
    output: a confusion matrix plot
    """
    
    from sklearn.metrics import plot_confusion_matrix
    import matplotlib.pyplot as plt
    import seaborn as sns
    plt.style.use('ggplot')

    ax = plot_confusion_matrix(estimator, 
                                X_test, 
                                y_test)
    plt.show()
    
def pairplot_helper(df):
    
    """
    input:  a plt.subplot object and a pandas dataframe
    output: a correlation plot 
    """
    
    import matplotlib.pyplot as plt
    import seaborn as sns
        
    sns.pairplot(df)
    plt.show()
    
def correlation_plotter(ax,df):
    
    """
    input:  a plt.subplot object, a pandas dataframe
    output: a correlation plot 
    """
    
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    ax = ax = sns.heatmap(df.drop(columns = 'match_id').corr(), 
                          cmap = 'coolwarm', 
                          square=True)

    ax.set_title('Correlation Matrix')
    
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
    
def roc_auc_plot(ax, estimators, X, y):
    '''
    Input:  plt.subplots object (ax),
            list of estimators (dictionary),
            X_train,X_test,y_train,y_test (lists)
    
    Output: plot of ROC AUC curves
    '''
    from sklearn.metrics import plot_roc_curve
    from sklearn.model_selection import train_test_split
    import matplotlib.pyplot as plt
    
    plt.style.use('ggplot')
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    for name, estimator in estimators.items():
        plot_roc_curve(estimator.fit(X_train,y_train),
                       X_test,
                       y_test,
                       alpha = 0.7,
                       ax = ax,
                       name = name)
    ax.set_title('ROC AUC Curves',fontsize=20)
    plt.show()