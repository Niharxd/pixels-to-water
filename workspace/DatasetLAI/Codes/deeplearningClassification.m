
%--------------------------------------------------------------------------
%LOAD DATA
%--------------------------------------------------------------------------
%Load image data
imagepath = fullfile('C:\Users\ronn\Documents\DLSU\Publications\Journals\CEA\extracted_vODGI_abc', 'imageClassification');
imds = imageDatastore(imagepath,...
    'IncludeSubfolders',true,...
    'LabelSource','FolderNames');

%Set an output function
imds.ReadFcn = @(loc)imresize(imread(loc),[331,331]);

%Split inputs intro training and validation sets
[imdsTrain,imdsValidation] = splitEachLabel(imds,0.8,'randomized');

% %Display some sample images
% numTrainImages = numel(imdsTrain.Labels);
% idx = randperm(numTrainImages,16);
% figure
% for i = 1:16
%     subplot(4,4,i)
%     I = readimage(imdsTrain,idx(i));
%     imshow(I)
% end

%--------------------------------------------------------------------------
%REPLACE FINAL LAYERS
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% LOAD PRETRAINED PRE-TRAINED DEEP LEARNING NETWORK
%--------------------------------------------------------------------------
model = "inceptionv3";                                                     %INPUT here what is the model to use

dagnet = inceptionv3;                                                      %INPUT here what is the model to use
lgraph = layerGraph(dagnet);

% Plots the network layers
%plot(lgraph)

%Display an interactive visualization of the network architecture and detailed information about the network layers.
%analyzeNetwork(net)

if model == "mobilenetv2"
    %lgraph = removeLayers(lgraph, {'Logits_softmax'});                    %remove second to the last layer which is a softmax layer
    
    newfc = fullyConnectedLayer(3,'Name','new_fully_connected',...
        'WeightLearnRateFactor',20,'BiasLearnRateFactor',20);
    lgraph = replaceLayer(lgraph,'Logits',newfc);                          %command dagnet.Layers to check the name of the fully connected layer
    
    newsoftmax = softmaxLayer('Name','new_softmax');
    lgraph = replaceLayer(lgraph,'Logits_softmax',newsoftmax);             %command dagnet.Layers to check the name of the classification output layer
    
    newclass = classificationLayer('Name','new_classification');
    lgraph = replaceLayer(lgraph,'ClassificationLayer_Logits',newclass);   %command dagnet.Layers to check the name of the classification output layer
    
    %     lgraph_new = connectLayers(lgraph,'new_fully_connected','new_softmax')
    %     lgraph_new = connectLayers(lgraph,'new_softmax','new_classification')
elseif model == "resnet101"
    newfc = fullyConnectedLayer(3,'Name','new_fully_connected',...
        'WeightLearnRateFactor',20,'BiasLearnRateFactor',20);
    lgraph = replaceLayer(lgraph,'fc1000',newfc);                          
    
    newsoftmax = softmaxLayer('Name','new_softmax');
    lgraph = replaceLayer(lgraph,'prob',newsoftmax);     
    
    newclass = classificationLayer('Name','new_classification');
    lgraph = replaceLayer(lgraph,'ClassificationLayer_predictions',newclass); 
elseif model == "inceptionv3"
    newfc = fullyConnectedLayer(3,'Name','new_fully_connected',...
        'WeightLearnRateFactor',20,'BiasLearnRateFactor',20);
    lgraph = replaceLayer(lgraph,'predictions',newfc);                          
    
    newsoftmax = softmaxLayer('Name','new_softmax');
    lgraph = replaceLayer(lgraph,'predictions_softmax',newsoftmax);     
    
    newclass = classificationLayer('Name','new_classification');
    lgraph = replaceLayer(lgraph,'ClassificationLayer_predictions',newclass); 
elseif model == "nasnetlarge"
    newfc = fullyConnectedLayer(3,'Name','new_fully_connected',...
        'WeightLearnRateFactor',20,'BiasLearnRateFactor',20);
    lgraph = replaceLayer(lgraph,'predictions',newfc);                          
    
    newsoftmax = softmaxLayer('Name','new_softmax');
    lgraph = replaceLayer(lgraph,'predictions_softmax',newsoftmax);     
    
    newclass = classificationLayer('Name','new_classification');
    lgraph = replaceLayer(lgraph,'ClassificationLayer_predictions',newclass); 
elseif model == "nasnet-mobile"
    newfc = fullyConnectedLayer(3,'Name','new_fully_connected',...
        'WeightLearnRateFactor',20,'BiasLearnRateFactor',20);
    lgraph = replaceLayer(lgraph,'Logits',newfc);                          
    
    newsoftmax = softmaxLayer('Name','new_softmax');
    lgraph = replaceLayer(lgraph,'Logits_softmax',newsoftmax);     
    
    newclass = classificationLayer('Name','new_classification');
    lgraph = replaceLayer(lgraph,'ClassificationLayer_Logits',newclass);     
end

%The first layer, the image input layer, requires input images of size 227-by-227-by-3, where 3 is the number of color channels.
inputSize = lgraph.Layers(1).InputSize

%--------------------------------------------------------------------------
%TRAIN NETWORK
%--------------------------------------------------------------------------
%The network requires input images of size 227-by-227-by-3, but the images in the image datastores have different sizes. Use an augmented image datastore to automatically resize the training images. Specify additional augmentation operations to perform on the training images: randomly flip the training images along the vertical axis, and randomly translate them up to 30 pixels horizontally and vertically. Data augmentation helps prevent the network from overfitting and memorizing the exact details of the training images.
pixelRange = [-30 30];
imageAugmenter = imageDataAugmenter( ...
    'RandXReflection',true, ...
    'RandXTranslation',pixelRange, ...
    'RandYTranslation',pixelRange);
augimdsTrain = augmentedImageDatastore(inputSize(1:2),imdsTrain, ...
    'DataAugmentation',imageAugmenter);

%To automatically resize the validation images without performing further data augmentation, use an augmented image datastore without specifying any additional preprocessing operations.
augimdsValidation = augmentedImageDatastore(inputSize(1:2),imdsValidation);

%Specify the training options. For transfer learning, keep the features from the early layers of the pretrained network (the transferred layer weights). To slow down learning in the transferred layers, set the initial learning rate to a small value. In the previous step, you increased the learning rate factors for the fully connected layer to speed up learning in the new final layers. This combination of learning rate settings results in fast learning only in the new layers and slower learning in the other layers. When performing transfer learning, you do not need to train for as many epochs. An epoch is a full training cycle on the entire training data set. Specify the mini-batch size and validation data. The software validates the network every ValidationFrequency iterations during training.
options = trainingOptions('sgdm', ...               % sgdm, rmsprop, adam
    'MiniBatchSize',10, ...
    'MaxEpochs',6, ...
    'InitialLearnRate',1e-4, ...
    'Shuffle','every-epoch', ...
    'ValidationData',augimdsValidation, ...
    'ValidationFrequency',3, ...
    'Verbose',1, ...
    'Plots','training-progress');

%Train the network that consists of the transferred and new layers. By default, trainNetwork uses a GPU if one is available (requires Parallel Computing Toolbox™ and a CUDA® enabled GPU with compute capability 3.0 or higher). Otherwise, it uses a CPU. You can also specify the execution environment by using the 'ExecutionEnvironment' name-value pair argument of trainingOptions.
%netTransfer = trainNetwork(augimdsTrain,layers,options);
%lgraph_2 is the exported model from deepNetworkDesigner with new
%fullyconnectlayer and classification layers at the network end section
netTransfer = trainNetwork(augimdsTrain,lgraph,options);

%--------------------------------------------------------------------------
%CLASSIFY VALIDATION IMAGES
%--------------------------------------------------------------------------
%Classify the validation images using the fine-tuned network.
[YPred,scores] = classify(netTransfer,augimdsValidation);

% %Display four sample validation images with their predicted labels.
% idx = randperm(numel(imdsValidation.Files),6);
% figure
% for i = 1:6
%     subplot(2,3,i)
%     I = readimage(imdsValidation,idx(i));
%     imshow(I)
%     Pred = YPred(idx(i));
%   %  TrueVal = scores(idx(i));
%     title(strcat('Predicted Class: ',string(label)));
% end

%Calculate the classification accuracy on the validation set. Accuracy is the fraction of labels that the network predicts correctly.
YValidation = imdsValidation.Labels;
accuracy = mean(YPred == YValidation)

%Network-predicted values
YPred

%True Value
%YValidation

%Display confusion matrix
figure(); ConfusionMat1 = confusionchart(YValidation,YPred,'RowSummary','row-normalized','ColumnSummary','column-normalized');
figure(); ConfusionMat2 = confusionchart(YValidation,YPred);
