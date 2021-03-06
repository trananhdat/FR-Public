class Parameters:

    url_recogition = "http://203.162.88.102:5000/recognition_v1"

    # url_recogition = "http://127.0.0.1:5000/recognition_v1"
    
    url_mode = 'http://203.162.88.102:5000/camid2mode/{}'
    
    url_mac2mode = "http://203.162.88.102:5000/mac2mode/{}"

    url_avt = "http://203.162.88.102:3000/img/avatar/{}.jpg"
    
    path_xml = 'haarcascades/haarcascade_frontalface_default.xml'
    
    path_lbp_xml = 'haarcascades/lbpcascade_frontalface.xml'

    # api
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'x-access-tokens' : 'ngoctuhan'}

    cameraId = None

    txt = "model/Slim-320/slim-320.prototxt"
    
    caffe = 'model/Slim-320/slim-320.caffemodel'

    color_history = 'white'
