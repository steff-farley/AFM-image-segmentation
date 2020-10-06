%%%
This code calculates the proportion of pixels that are different between
two binary images. This can be used to determine how many pixels change
when artificial noise is added. Noise augmented images must be named the
same as their respective original images. Takes two paths to folders
containing original and noise augmented images, calculates the proportion
of pixels that change in the noise augmented images.

Input paths are specified on lines 17 and 24. Output path specified on
line 46.

The name of the outputted dataset is specified on line 48.
%%%
cd('/home/marmf/Deposition images/Code');

%% load original images
D = imageDatastore('/home/marmf/Deposition images/Images/Testing impact of noise/Originals/Localm','FileExtensions','.png','IncludeSubfolders',true,'LabelSource','foldernames');
D2 = readall(D);
paths2D = D.Files;

D = D2;

%% load noise augmented images
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
