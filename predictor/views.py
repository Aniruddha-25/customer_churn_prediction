from django.shortcuts import render
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import os
from django.conf import settings
import json

# Create your views here.

def train_model(request):
    """Train machine learning models and display results"""
    context = {}
    
    if request.method == 'POST':
        try:
            # Load dataset
            dataset_path = os.path.join(settings.BASE_DIR, 'predictor', 'dataset', 'Customertravel.csv')
            data = pd.read_csv(dataset_path)
            
            # Data preprocessing - Convert categorical variables to numerical
            data["FrequentFlyer"] = data["FrequentFlyer"].map({"Yes": 2, "No": 1, "No Record": 0})
            data["AnnualIncomeClass"] = data["AnnualIncomeClass"].map(
                {"Low Income": 1, "Middle Income": 2, "High Income": 3}
            )
            data["AccountSyncedToSocialMedia"] = data["AccountSyncedToSocialMedia"].map(
                {"Yes": 1, "No": 0}
            )
            data["BookedHotelOrNot"] = data["BookedHotelOrNot"].map({"Yes": 1, "No": 0})
            
            # Select features (X) and target variable (y)
            x = data[
                [
                    "Age",
                    "FrequentFlyer",
                    "AnnualIncomeClass",
                    "ServicesOpted",
                    "AccountSyncedToSocialMedia",
                    "BookedHotelOrNot",
                ]
            ]
            y = data["Target"]
            
            # Split data into training and testing sets (80-20 split)
            x_train, x_test, y_train, y_test = train_test_split(
                x, y, test_size=0.2, random_state=42
            )
            
            models = {
                "Logistic Regression": LogisticRegression(max_iter=1000),
                "Decision Tree": DecisionTreeClassifier(random_state=42),
                "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
            }
            
            # Train and evaluate each model
            results = {}
            
            for name, model in models.items():
                model.fit(x_train, y_train)
                y_pred = model.predict(x_test)
                acc = accuracy_score(y_test, y_pred)
                results[name] = round(acc * 100, 2)
            
            best_model_name = max(results, key=results.get)
            
            context['results'] = results
            context['best_model'] = best_model_name
            
        except FileNotFoundError:
            context['error'] = 'Dataset file not found. Please ensure Customertravel.csv is in predictor/dataset/ folder.'
        except Exception as e:
            context['error'] = f'An error occurred: {str(e)}'
    
    return render(request, 'predictor/train.html', context)


def predict_churn(request):
    """Generate pie chart for customer churn analysis based on age range"""
    context = {}
    
    if request.method == 'POST':
        try:
            start_age = int(request.POST.get('start_age'))
            end_age = int(request.POST.get('end_age'))
            
            if start_age > end_age:
                context['error'] = 'Starting age must be less than or equal to ending age.'
                return render(request, 'predictor/predict.html', context)
            
            # Load dataset
            dataset_path = os.path.join(settings.BASE_DIR, 'predictor', 'dataset', 'Customertravel.csv')
            data = pd.read_csv(dataset_path)
            
            # Create churn status labels for visualization
            data["ChurnStatus"] = data["Target"].map({0: "Stayed", 1: "Left"})
            
            # Filter data based on age range
            filtered_data = data[(data["Age"] >= start_age) & (data["Age"] <= end_age)]
            
            if filtered_data.empty:
                context['error'] = f'No data found for age range {start_age} to {end_age}.'
                return render(request, 'predictor/predict.html', context)
            
            churn_counts = filtered_data["ChurnStatus"].value_counts()
            
            # Prepare data for JavaScript
            chart_data = {
                'labels': churn_counts.index.tolist(),
                'values': churn_counts.values.tolist()
            }
            
            context['chart_data'] = json.dumps(chart_data)
            context['start_age'] = start_age
            context['end_age'] = end_age
            
        except ValueError:
            context['error'] = 'Please enter valid age values.'
        except FileNotFoundError:
            context['error'] = 'Dataset file not found. Please ensure Customertravel.csv is in predictor/dataset/ folder.'
        except Exception as e:
            context['error'] = f'An error occurred: {str(e)}'
    
    return render(request, 'predictor/predict.html', context)
