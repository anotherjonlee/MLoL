def plot_cm(ax, estimator, X_test, y_test):
    
    """
    input:  a plt.subplot object, an estimator object, X_test array, y_test array
    output: a confusion matrix plot
    """
    
    from sklearn.metrics import plot_confusion_matrix
    import matplotlib.pyplot as plt
    import seaborn as sns
    %matplotlib inline
    plt.style.use('ggplot')

    disp = plot_confusion_matrix(classifier, X_test, y_test,
                                display_labels=class_names,
                                cmap=plt.cm.Blues,
                                normalize=normalize)
    plt.show()
    
def general_correlation_plot(ax,df):
    
    """
    input:  a plt.subplot object and a pandas dataframe
    output: a correlation plot 
    """
    
    import matplotlib.pyplot as plt
    import seaborn as sns
    %matplotlib inline
    plt.style.use('ggplot')
    
    ax = sns.pairplot(df,
                      corner = True,
                      hue = 'teams')
    plt.show()
    
def granular_correlation_plot(ax,df, var1, var2, var3 = None):
    
    """
    input:  a plt.subplot object, a pandas dataframe, feature names (string)
    output: a correlation plot 
    """
    
    import matplotlib.pyplot as plt
    import seaborn as sns
    %matplotlib inline
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
    ax = sns.boxplot(x = x, 
                     y = y, 
                     data = df,
                     hues = hue_var,
                     orient = 'h')
    plt.show()