cd('/home/marmf/Deposition images/Code');

%% load images
D = imageDatastore('/home/marmf/Deposition images/Images/Testing impact of noise/Originals/Localm','FileExtensions','.png','IncludeSubfolders',true,'LabelSource','foldernames');
D2 = readall(D);
paths2D = D.Files;

D = D2;

E = imageDatastore('/home/marmf/Deposition images/Images/Testing impact of noise/Banding/Localm','FileExtensions','.png','IncludeSubfolders',true,'LabelSource','foldernames');
E2 = readall(E);
paths2E = E.Files;

E = E2;

Num = length(D);
pixdiff = zeros(Num,1);


for i = 1:Num
    B = D{i};
    C = E{i};
    %% make sure images are binary
    B2 = imbinarize(B);
    
    C2 = imbinarize(C);
    
    Z = imabsdiff(B2,C2); % Z is a matrix of equal size to image with values 1 if pixels are different and 0 ow
    pixdiff(i) = sum(Z,'All')/numel(C2); % sum all values in Z (total number of pixels that were different)
end

cd('/home/marmf/Deposition images/Images/Testing impact of noise/Banding/Localm');

save('pixdiff_banding_lm','pixdiff')
