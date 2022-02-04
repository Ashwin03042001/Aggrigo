import json
import pickle

__recomended_crop_index=None
__recomended_crop=None
__crop_dict=None

def get_recommended_crop(Nitrogen,Phosphorous,Potassium,temperature,humidity,ph,rainfall):
    global __crop_dict
    global __recomended_crop
    global __recomended_crop_index

    with open(r'A:\cn\crops\crops\aggrigo\crop_recommendation.pickle', "rb") as f:
        model=pickle.load(f)

    with open(r"A:\cn\crops\crops\aggrigo\crop_identification.json", "r") as f:
        __crop_dict=json.load(f)

    return (__crop_dict[str(model.predict([[Nitrogen,Phosphorous,Potassium,temperature,humidity,ph,rainfall]]).tolist()[0])])

if __name__=="__main__":
    get_recommended_crop(90,42,43,20.87974371,82.00274423,6.502985292,202.9355362)