def feature_separator(df):
    """
    The function takes a dataframe and separates its columns into
    lists of numeric and categorical columns
    
    input:  pandas dataframe
    output: a list of numeric columns and 
            a list of categorical columns
    """
    numeric_features = []
    cat_features = []

    for col in df.columns:
        if df[col].dtype == 'int64':
            numeric_features.append(col)
        else:
            cat_features.append(col)
    return numeric_features,cat_features

def pipeline(numeric_features = False, 
             numeric_feature_names = [],
             cat_features = False,
             cat_feature_names = [],
             normalize = True):
    """
    The function takes names of numeric and categorical features
    from a dataframe and transform the dataframe and builds a 
    base pipeline for any estimators.
    
    input:  numeric features in df (bool)
            categorical features in df (bool)
            **kargs ({'num_features': (list),'cat_features':(list)})   
    
    output: Pipeline object with imputed and scaled numeric features
            and imputed and one hot encoded categorical features      
    """
    from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
    from sklearn.pipeline import Pipeline
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    
    base_transformer = ColumnTransformer(transformers=[])

    if numeric_features == True:
        # Numeric features pipeline
        
        # Scale and normalize numeric values
        if normalize == True:
            num_processor = Pipeline(steps=[
                ('num_imputer',SimpleImputer(strategy='mean')),
                ('scaler',StandardScaler())
            ])
        
        else:
            num_processor = Pipeline(steps=[
                ('num_imputer',SimpleImputer(strategy='mean')),
                ('scaler',StandardScaler())
            ])
        # Append the numeric pipeline to the base_transformer
        base_transformer.transformers.append(('numeric',
                                              num_processor,
                                              numeric_feature_names))
        
    if cat_features == True:
        # Categorical features pipeline
        cat_processor = Pipeline(steps=[
            ('cat_imputer',SimpleImputer(strategy='most_frequent')),
            ('encoder',OneHotEncoder(handle_unknown='ignore'))
        ])
        
        # Append the categorical pipeline to the base_transformer
        base_transformer.transformers.append(('categorical',
                                              cat_processor,
                                              cat_feature_names))

    # Final base pipeline
    if numeric_features == True or cat_features == True:
        base_pipeline = Pipeline(steps=[('transformer',
                                         base_transformer)])
    
    else:
        base_pipeline = Pipeline(steps = [])
    
    return base_pipeline

def append_model(estimator,base_pipeline):
    """
    input:  machine learning estimator method, 
            pipeline object
    
    output: pipeline object with an appended estimator
    """
    
    from sklearn.base import clone
    
    pipeline = clone(base_pipeline)
    pipeline.steps.append(('estimator', estimator))
    
    return pipeline

def model_scorer(estimators,X_train,y_train,X_test,y_test):
    """
    input:  estimators (dictionary)
    output: print scores
    """
    from sklearn.metrics import precision_score, recall_score
    from sklearn.model_selection import cross_val_score
    
    for name, estimator in estimators.items():
        
        pred = estimator.fit(X_train,y_train).predict(X_test)
    
        print(f'Mean cross validatin score for {name}: {cross_val_score(estimator,X_train,y_train).mean():.2f}')
        print(f'Precision score for {name}: {precision_score(y_test, pred):.2f}')
        print(f'Recall score for {name}: {recall_score(y_test, pred):.2f}')
        print('\n')
