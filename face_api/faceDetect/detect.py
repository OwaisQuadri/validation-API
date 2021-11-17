# facial recognition implementation
import face_recognition as fr
from PIL import Image
import os
from os import path
import urllib.request as request
from django.conf import settings
from ..models import Face
import socket
from io import BytesIO


# face_recognition --tolderance .40 ./known ./input
class Detect:
    def __init__(self):
        pass
    def recognize(self):
        #init inputFaces
        inputFaces=[]
        #init output
        output=""
        # initialize recognized
        recognized = ""
        # load image to save
        FMR=settings.MEDIA_ROOT
        FM=settings.MEDIA_ROOT / settings.MEDIA_URL
        # if not settings.IS_WIN:
        #     imagesDir=imagesDir.replace("\\","/")
        # head=os.path.dirname(settings.BASE_DIR)+ imagesDir# fixes when system changes
        known_path_FM=path.join('images','known')
        # get faces of random pic input
        input_image_path=FMR / str(Face.objects.last().face)
        input_image = fr.load_image_file(input_image_path)
        known_faces=Face.objects.filter(known=True)
        # get faces from input
        input_locations = fr.face_locations(input_image)
        numOfInputs = len(input_locations)
        count = 0
        for input in input_locations:
            count += 1
            top, right, bottom, left = input
            face_input = input_image[top:bottom, left:right]
            pil_image = Image.fromarray(face_input)
            # pil_image.show()
            # inputFaces.append(pil_image)
            # inputcount_path=FM / 'images' / 'input' / str(f'input{count}.png')
            # pil_image.save(inputcount_path)
        self.delete_unknowns()
        # get face encoding of knowns
        print ("Known users:")
        # knownPics = os.listdir(settings.API_LINK+path.join(head,knownPics_path))
        for f in known_faces:
            
            name_of_known = str(f.name)
            print(name_of_known)
            known_path=FMR / str(f.face)
            image_of_known = fr.load_image_file(known_path)
            known_face_encoding = fr.face_encodings(image_of_known)[0]

            # compare current known against inputs
            # inputLocation_path="images\\input"
            # inputLocation = os.listdir(settings.API_LINK+path.join(head,inputLocation_path))
            
            for i in inputFaces:
                # i_path=f'images\\input\\{i}'
                # if not settings.IS_WIN:
                #     i_path=i_path.replace("\\","/")
                
                # i__path=settings.API_LINK+path.join(head,i_path)
                
                # img = fr.load_image_file(i__path)
                img = fr.load_image_file(i)
                # im=Image.open(i)
                
                # w,h=im.size
                # kfl=[(0, w, h, 0)]
                # im.close()
                face_encoding = fr.face_encodings(img)#,known_face_locations=kfl)
                
                match = fr.compare_faces(known_face_encoding, face_encoding)[0]
                
                if match == True:
                    print("recognized!")
                    output+= name_of_known.replace("_"," ")+","
        try:
            if output[-1]==",":
                output=output[:-1]
        except:
            output=""
        return output
    def delete_unknowns(self):
        unknowns=Face.objects.filter(known=False)
        for this in unknowns:
            this.face.delete()
        unknowns.delete()
        #numOfFaces = len(facelocations)
        # if(numOfFaces > 1):
        #   print(f'there are {numOfFaces} faces in this image')
        # loop through face locations


        # recieves a picture with a mode [save, predict]

        # if save, save picture to the 'known' folder
        # else save to 'input' folder and run facialrecog against the picture in comparison to the known folder
