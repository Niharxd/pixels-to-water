% System initialization
clear; clc;

%--------------------------------------------------------------------------
% LOAD DATA
%--------------------------------------------------------------------------
% Load complete predictor and response data from the xlsx file
dataset = readtable('data_classification.xlsx','Sheet','tgi');         % The corresponding file must have the image directory on the first column and the target numerical value on the second column
morphdata = dataset(:,1:4);

% Load training data and split 80% from the total count
[m,n] = size(morphdata);
P = 0.56;
idx = randperm(m);
trainingdata = morphdata(idx(1:round(P*m)),:);

% Load testing data and split 20% from the total count
testdata = morphdata(idx(round(P*m)+1:end),:);
[k,l] = size(testdata);
Q = 0.45;
idz = randperm(k);
testingdata = testdata(idz(1:round(Q*k)),:);

% Load training data and split 80% from the total count
validationdata = trainingdata(idz(round(Q*k)+1:end),:);


% Separate the variables for test images and corresponding target value
% Training
train_predictors = trainingdata(:,2:4);
train_growthstage = table2array(trainingdata(:,1:1));

% Validation
valid_predictors = validationdata(:,2:4);
valid_growthstage = table2array(validationdata(:,1:1));

% Testing
test_predictors = testingdata(:,2:4);
test_growthstage = table2array(testingdata(:,1:1));

%--------------------------------------------------------------------------
% DEFAULT MODEL TRAINING
%--------------------------------------------------------------------------
% Unoptimized model

model = "knn"                                                              % CHANGE
X = train_predictors;
Y = train_growthstage                                                    % CHANGE

if model == "tree"
    Mdl1 = fitctree(X,Y)
    YPred = predict(Mdl1,X)
elseif model == "nb"
    Mdl1 = fitcnb(X,Y)
    YPred = predict(Mdl1,X)
elseif model == "discri"
    Mdl1 = fitcdiscr(X,Y)
    YPred = predict(Mdl1,X)
elseif model == "knn"
    Mdl1 = fitcknn(X,Y)
    YPred = predict(Mdl1,X)
end


figure(); ConfusionMat1 = confusionchart(Y,YPred,'RowSummary','row-normalized','ColumnSummary','column-normalized');

%--------------------------------------------------------------------------
% OPTIMIZATION
%--------------------------------------------------------------------------

if model == "tree"
    Mdloptim = fitctree(X,Y,...
        'OptimizeHyperparameters','auto',...
        'HyperparameterOptimizationOptions',struct('AcquisitionFunctionName','expected-improvement-plus'))
elseif model == "nb"
    Mdloptim = fitcnb(X,Y,...
        'OptimizeHyperparameters','auto',...
        'HyperparameterOptimizationOptions',struct('AcquisitionFunctionName','expected-improvement-plus'))
elseif model == "discri"
    Mdloptim = fitcdiscr(X,Y,...
        'OptimizeHyperparameters','auto',...
        'HyperparameterOptimizationOptions',struct('AcquisitionFunctionName','expected-improvement-plus'))
elseif model == "knn"
    Mdloptim = fitcknn(X,Y,...
        'OptimizeHyperparameters','auto',...
        'HyperparameterOptimizationOptions',struct('AcquisitionFunctionName','expected-improvement-plus'))
end

%--------------------------------------------------------------------------
% OPTIMIZED MODEL VALIDATION
%--------------------------------------------------------------------------

X = valid_predictors;
YTrue = valid_growthstage                                                      % CHANGE

YPred = predict(Mdloptim,X)
figure(); ConfusionMat1 = confusionchart(YTrue,YPred,'RowSummary','row-normalized','ColumnSummary','column-normalized');

%--------------------------------------------------------------------------
% TESTING USING THE OPTIMIZED MODEL
%--------------------------------------------------------------------------


X = test_predictors;
YTrue = test_growthstage                                                        % CHANGE

Mdltest = Mdloptim;

YPred = predict(Mdltest,X)


figure(); ConfusionMat1 = confusionchart(YTrue,YPred,'RowSummary','row-normalized','ColumnSummary','column-normalized');
figure(); ConfusionMat2 = confusionchart(YTrue,YPred);
