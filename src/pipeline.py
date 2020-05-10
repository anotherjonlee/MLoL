from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.base import clone
from sklearn.impute import SimpleImputer

def pipeline(numeric_features = False, 
             numeric_feature_names = [],
             cat_features = False,
             cat_feature_names = []):
    """
    The function takes names of numeric and categorical features
    from a dataframe and transform the dataframe and builds a 
    base pipeline for any estimators.
    
    input:  numeric features in df (bool)
            categorical features in df (bool)
            names of numeric features (list)
            names of categorical features (list)   
    
    output: Pipeline object with imputed and scaled numeric features
            and imputed and one hot encoded categorical features      
    """
    
    base_transformer = ColumnTransformer(transformers=[])

    if numeric_features == True:
        # Numeric features pipeline
        num_processor = Pipeline(steps=[
            ('num_imputer',SimpleImputer(strategy='mean')),
            ('scaler',StandardScaler())
        ])
        
        # Append the numeric pipeline to the base_transformer
        base_transformer.transformers.append(('numeric',num_processor,numeric_feature_names))
        
    if cat_features == True:
        # Categorical features pipeline
        cat_processor = Pipeline(steps=[
            ('cat_imputer',SimpleImputer(strategy='most_frequent')),
            ('encoder',OneHotEncoder(handle_unknown='ignore'))
        ])
        # Append the categorical pipeline to the base_transformer
        base_transformer.transformers.append(('categorical',cat_processor,cat_feature_names))

    # Final base pipeline
    if numeric_features == True or cat_features == True:
        base_pipeline = Pipeline(steps=[('transformer',base_transformer)])
    
    else:
        base_pipeline = Pipeline(steps = [])
    
    return base_pipeline