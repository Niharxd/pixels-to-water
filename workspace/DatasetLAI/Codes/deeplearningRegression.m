% System initialization
clear; clc;

%--------------------------------------------------------------------------
% LOAD DATA
%--------------------------------------------------------------------------
% Load complete image file name and target data from the xlsx file
dataset = readtable('data_imageRegression.xlsx','Sheet','Sheet1');         % The corresponding file must have the image directory on the first column and the target numerical value on the second column
morphdata = dataset(:,1:2);

% Load training data and split 80% from the total count
[m,n] = size(morphdata);
P = 0.80;
idx = randperm(m);
trainingdata = morphdata(idx(1:round(P*m)),:);

% Load testing data and split 20% from the total count
testdata = morphdata(idx(round(P*m)+1:end),:);
[k,l] = size(testdata);
Q = 0.2;
idz = randperm(k);
testingdata = testdata(idz(1:round(Q*k)),:);

% Load training data and split 80% from the total count
validationdata = trainingdata(idz(round(Q*k)+1:end),:);

% Separate the variables for test images and corresponding target value
test_img = testingdata(:,1:1);
test_trueValue = testingdata(:,2:2);
%--------------------------------------------------------------------------
% LOAD PRETRAINED MODEL
%--------------------------------------------------------------------------
% Initialize pre-trained deep learning model
dagnet = mobilenetv2;                                                        % INPUT here what is the model to use
lgraph = layerGraph(dagnet);

% Plots the network layers
%plot(lgraph)

%--------------------------------------------------------------------------
% REPLACE FINAL LAYERS AND ADD NEW FULLY CONNECTED AND REGRESSION LAYERS
%--------------------------------------------------------------------------
model = "inceptionv3";                                                       % INPUT here what is the model to use

if model == "mobilenetv2"
    lgraph = removeLayers(lgraph, {'Logits_softmax'});                     % Remove second to the last layer which is a softmax layer
    
    newfc = fullyConnectedLayer(1,'Name','fc');
    lgraph = replaceLayer(lgraph,'Logits',newfc);                          % Command dagnet.Layers to check the name of the fully connected layer
    newreg = regressionLayer('Name','NewReg');
    lgraph = replaceLayer(lgraph,'ClassificationLayer_Logits',newreg);     % Command dagnet.Layers to check the name of the classification output layer
    newlgraph = connectLayers(lgraph,'fc','NewReg')
elseif model == "resnet101"
    lgraph = removeLayers(lgraph, {'prob'});
    
    newfc = fullyConnectedLayer(1,'Name','fc');
    lgraph = replaceLayer(lgraph,'fc1000',newfc);
    newreg = regressionLayer('Name','NewReg');
    lgraph = replaceLayer(lgraph,'ClassificationLayer_predictions',newreg);
    newlgraph = connectLayers(lgraph,'fc','NewReg')
elseif model == "inceptionv3"
    lgraph = removeLayers(lgraph, {'predictions_softmax'});
    
    newfc = fullyConnectedLayer(1,'Name','fc');
    lgraph = replaceLayer(lgraph,'predictions',newfc);
    newreg = regressionLayer('Name','NewReg');
    lgraph = replaceLayer(lgraph,'ClassificationLayer_predictions',newreg);
    newlgraph = connectLayers(lgraph,'fc','NewReg')
elseif model == "inceptionresnetv2"
    lgraph = removeLayers(lgraph, {'predictions_softmax'});
    
    newfc = fullyConnectedLayer(1,'Name','fc');
    lgraph = replaceLayer(lgraph,'predictions',newfc);
    newreg = regressionLayer('Name','NewReg');
    lgraph = replaceLayer(lgraph,'ClassificationLayer_predictions',newreg);
    newlgraph = connectLayers(lgraph,'fc','NewReg')
else
    x = "add new model"
end

%--------------------------------------------------------------------------
% TRAIN NETWORK
%--------------------------------------------------------------------------
inputSize = newlgraph.Layers(1).InputSize

pixelRange = [-30 30];

imageAugmenter = imageDataAugmenter( ...
    'RandXReflection',true, ...
    'RandXTranslation',pixelRange, ...
    'RandYTranslation',pixelRange);

augimdsTrain = augmentedImageDatastore(inputSize(1:2),trainingdata,...
    'DataAugmentation',imageAugmenter);

augimdsValidation = augmentedImageDatastore(inputSize(1:2),validationdata,...
    'DataAugmentation',imageAugmenter);

% Configure the model hyperparameters
options = trainingOptions('sgdm',...
    'MiniBatchSize',20,...
    'MaxEpochs',7,...
    'InitialLearnRate',0.0001,...
    'LearnRateSchedule','piecewise',...
    'LearnRateDropFactor',0.1,...
    'LearnRateDropPeriod',20,...
    'Shuffle','every-epoch',...
    'ValidationFrequency',3,...
    'ValidationData', augimdsValidation,...
    'Plots','training-progress',...
    'Verbose',true);

% Model training
netTransfer = trainNetwork(augimdsTrain,newlgraph,options)

%--------------------------------------------------------------------------
% EVALUATE TEST IMAGES
%--------------------------------------------------------------------------
% Resize test images based on the pre-trained model required input image
% size
augimdsTesting = augmentedImageDatastore(inputSize(1:2),test_img, ...
    'DataAugmentation',imageAugmenter);

% Predict using the developed model and augmented test images
YPred = predict(netTransfer,augimdsTesting)

% Output the corresponding test true numerical value for test images
YTrue = table2array(test_trueValue)


% Visualization basic (alter using matlab gui) 
figure(); plot(1:length(YTrue),YTrue,'black+', 1:length(YPred),YPred,'bx');
ylabel('Fresh weight (grams)');
xlabel('Sample');
legend('Target fresh weight', strcat(model,' prediction'));
