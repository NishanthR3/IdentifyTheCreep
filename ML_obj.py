import librosa, pickle
UPLOAD_FOLDER = './uploads'

class ML_obj:
    """The Machine learning clustering algorithm that reports percentage similarity
        of two audio files"""

    def __init__(self):
        """Load the trained machine learning object"""
        pickle_file = open("clt.pickle", "rb")
        self.clt = pickle.load(pickle_file)
        pickle_file.close()

    def __load_audio(self, filename1, filename2):
        """Use Librosa to convert audio files to list and use the same sampling
            rate for both files"""
        data1, sr1 = librosa.load(UPLOAD_FOLDER+'/'+filename1, sr=None)
        data2, sr2 = librosa.load(UPLOAD_FOLDER+'/'+filename2, sr=None)
        if sr1 != sr2:
            sr_min = min(sr1, sr2)
            data1, sr1 = librosa.load(UPLOAD_FOLDER+'/'+filename1, sr=sr_min)
            data2, sr2 = librosa.load(UPLOAD_FOLDER+'/'+filename2, sr=sr_min)

        """Extract the mfcc features of both audio files. If number of mfcc
            coefficients are different, raise exception"""
        mfcc_mat1 = librosa.feature.mfcc(y=data1, sr=sr1)
        mfcc_mat2 = librosa.feature.mfcc(y=data2, sr=sr2)
        test1 = list()
        test2 = list()
        if len(mfcc_mat1) != len(mfcc_mat2):
            raise Exception()

        """Reformat the mfcc matrix"""
        for i in range(len(mfcc_mat1[0])):
            temp = list()
            for j in range(len(mfcc_mat1)):
                temp.append(mfcc_mat1[j][i])
            test1.append(temp)

        for i in range(len(mfcc_mat2[0])):
            temp = list()
            for j in range(len(mfcc_mat2)):
                temp.append(mfcc_mat2[j][i])
            test2.append(temp)
        return test1, test2

    def get_percentage(self, filename1, filename2):
        """Get the mfcc features for both files and predict clusters for each
            of the samples for each of the audio files"""
        test1, test2 = self.__load_audio(filename1, filename2)
        pred1 = self.clt.predict(test1)
        pred2 = self.clt.predict(test2)

        """Find percentage similarity between the samples' clusters"""
        ans = 0
        for i in range(min(len(pred1),len(pred2))):
            if pred1[i] == pred2[i]:
                ans += 1
        maximum = max(len(pred1),len(pred2))
        return ((ans/maximum) * 100)
