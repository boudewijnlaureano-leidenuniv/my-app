import optuna  
from xgboost import QuantileDMatrix, train  
from sklearn.metrics import accuracy_score, f1_score, classification_report, fbeta_score, confusion_matrix 
from sklearn.model_selection import cross_val_score   
import seaborn as sns  
import matplotlib.pyplot as plt  
import numpy as np  

  
class XGBoostModel:  
  
    def __init__(self):  
        optuna.logging.set_verbosity(optuna.logging.WARNING)  
  
    def print_multiple_metricf_values(self, y_test, y_pred):  
        print(f'F1 score: {f1_score(y_test, y_pred)}')  
        print(f'Classification report: {classification_report(y_test, y_pred)}')  
        print(f'accuracy report: {accuracy_score(y_test, y_pred)}')  
  
    def plot_confusion_matrix(self, conf_matrix):  
        plt.figure(figsize=(3, 3))  
        sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar=False,  
                    xticklabels=['Predicted No Churn', 'Predicted Churn'],  
                    yticklabels=['Actual Churn', 'Actual Churn'],  
                    linewidths=0.5, linecolor='red', square=True)  
        plt.title('New model', fontsize=10)  
        plt.xticks(fontsize=6)  
        plt.yticks(fontsize=6)  
        plt.show()  
 
    def train_and_validate_xgboost(self, X_train, X_test, y_train, y_test, objective):  
            
            study = optuna.create_study(direction='maximize')  
            study.optimize(objective, n_trials=25)  
    
            dtest = QuantileDMatrix(X_test, y_test)  
            dtrain = QuantileDMatrix(X_train, y_train)  
    
            best_params = study.best_params  
            best_score = study.best_value  
            
            print("Best F1 Score:", best_score)  
            print("Best Parameters:", best_params)  
    
            watchlist = [(dtrain, 'train'), (dtest, 'eval')]  
            best_params["tree_method"] = "hist"  
            best_params["objective"] = 'binary:logistic'  
            best_params["eval_metric"] = 'logloss'  
            early_stopping_rounds = 50  
            model = train(best_params, dtrain, num_boost_round=100, evals=watchlist,  
                        early_stopping_rounds=early_stopping_rounds, verbose_eval=False)  
    
            y_pred_prob = model.predict(dtest)  
    
            fbeta_scores = []  
            thresholds = np.arange(0.1, 1.0, 0.01)  
            for threshold in thresholds:  
                y_pred_binary = [1 if pred > threshold else 0 for pred in y_pred_prob]  
                fbeta_scores.append(fbeta_score(y_test, y_pred_binary, beta=1))  
            
            best_threshold = thresholds[np.argmax(fbeta_scores)]  
            y_pred_binary = [1 if pred > best_threshold else 0 for pred in y_pred_prob]  
            
            conf_matrix = confusion_matrix(y_test, y_pred_binary)  
    
            print(f'Best threshold: {best_threshold}')  
            self.print_multiple_metricf_values(y_test, y_pred_binary)  
            
            self.plot_confusion_matrix(conf_matrix)  
  
# Usage  
# model = XGBoostModel()  
# model.train_and_validate_xgboost(X_train, X_test, y_train, y_test, objective)  
