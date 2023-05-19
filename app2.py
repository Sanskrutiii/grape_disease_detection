import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image


st.set_option('deprecation.showfileUploaderEncoding', False)

# @st.cache(allow_output_mutation=True)
def load_model():
    model = tf.keras.models.load_model('./grapes.h5')
    return model

def predict_class(image, model):
    image = tf.cast(image, tf.float32)
    image = tf.image.resize(image, [256, 256])
    image = np.expand_dims(image, axis=0)
    prediction = model.predict(image)
    return prediction

def get_treatment_recommendation(result):
    if result == 'Black Rot':
        return '''Identification
Symptoms of black rot first appear as small yellowish spots on leaves. As the spots
(lesions) enlarge, a dark border forms around the margins. The centers of the lesions
become reddish brown. By the time the lesions reach 1/8 to 1/4 inch in diameter
(approximately two weeks after infection), minute black dots appear. These are fungal
fruiting bodies (pycnidia) and contain thousands of summer spores (conidia). Pycnidia
are often arranged in a ring pattern, just inside the margin of the lesions. Lesions may
also appear on young shoots, cluster stems, and tendrils. The lesions are purple to black,
oval in outline, and sunken. Pycnidia also form in these lesions. Fruit symptoms often do
not appear until the berries are about half grown. Small, round, light-brownish spots form
on the fruit. The rotted tissue in the spot softens, and becomes sunken. The spot enlarges
quickly, rotting the entire berry in a few days. The diseased fruit shrivels, becoming
small, hard, black and wrinkled (mummies). Tiny black pycnidia are also formed on the
fruit mummies. The mummies usually remain attached to the cluster.

Control : Control
Black rot can be very difficult control and there is no one method, including the use of
fungicides, that will control it alone. You need to develop and use an integrated disease
control program that uses some very important cultural practices combined with the
application of effective fungicides. If you think that fungicides alone will provide
complete control without the use of cultural practices, you will probably not be successful
in controlling this disease. For example, if your vines are located in the shade where they
do not dry rapidly, and you do not remove mummies and other infected tissues from the
vines during the dormant season, your chances of effectively controlling black rot are not
good, even with the use of effective fungicides'''

    elif result == 'Esca':
        return '''ESCA 
        Management
        Although preventative practices are most effective in young vineyards (before the vines become infected by trunk diseases), these practices have some utility in diseased mature vineyards. Wood cankers are very localized, thus protecting more pruning wounds means fewer new cankers each year resulting in fewer dead spurs, arms or canes over time.
        Post-infection practices (sanitation and vine surgery) for use in diseased, mature vineyards are not as effective and are far more costly than adopting preventative practices (delayed pruning, double pruning, and applications of pruning-wound protectants) in young vineyards. Nonetheless, sanitation and vine surgery may help maintain yields. In spring, look for dead spurs or for stunted shoots. Later in summer, when there is a reduced chance of rainfall, practice good sanitation by cutting off these cankered portions of the vine beyond the canker, to where wood appears healthy. Then remove diseased, woody debris from the vineyard and destroy it. 
        In addition to the fungicides labeled as pruning-wound protectants, consider using alternative materials, such as a wound sealant with 5% boric acid in acrylic paint (Tech-Gro B-Lock), which is effective against Eutypa dieback and Esca, or an essential oil (Safecoat VitiSeal).
        Identification
        Eutypa dieback, Botryosphaeria dieback, Esca, and Phomopsis dieback make up a complex of "trunk diseases" caused by different wood-infecting fungi. Eutypa dieback delays shoot emergence in spring, and the shoots that eventually do grow have dwarfed, chlorotic leaves, sometimes with a cupped shape and/ or tattered margins. Symptomatic shoots are likely to either die back later that growing season or the spur from which they originate will die the following year. Eutypa dieback causes death of spurs, arms, cordons, canes, and sometimes the upper section of the trunk, depending on the location of the wood canker. Wedge-shaped wood cankers form in infected wood and are indistinguishable from those associated with Botryosphaeria dieback and Phomopsis dieback. Dead spurs and shoot dieback caused by Eutypa dieback are canopy symptoms shared in common among multiple trunk diseases, which often occur in mixed infection within the vineyard and even within an individual vine.'''
    elif result == 'Leaf Blight':
        return '''
        Identification
        It appears in the month of June and December. The disease attacks both leaves and fruits. Small
        yellowish spots first appear along the leaf margins, which gradually enlarge and turn into brownish
        patches with concentric rings. Severe infection leads to drying and defoliation of leaves. Symptoms in
        the form of dark brown-purplish patches appear on the infected berries, rachis and bunch stalk just
        below its attachment with the shoots.
        
        Control : If the disease on the berries is not controlled in the field, it can lead to berry rotting during
        transit and storage. Bordeaux mixture (1.0%), Mancozeb (0.2%), Topsin-M (0.1%), Ziram (0.35%) or
        Captan (0.2%) is to be sprayed alternatively at weekly intervals from Jun-August and again from
        December until harvest to keep this disease under check. Two to three sprays of systemic fungicides
        should be given per season.'''
    
    elif result == 'Healthy':
        st.balloons()
        return 'No treatment needed. The leaf is healthy.'
    else:
        return 'Unknown disease. Consult an expert for proper treatment.'

model = load_model()
st.title('Grape Leaf Disease Detector')

file = st.file_uploader("Upload an image of a flower", type=["jpg", "png"])

if file is None:
    st.text('Waiting for upload....')
else:
    slot = st.empty()
    slot.text('Running inference....')

    test_image = Image.open(file)
    st.image(test_image, caption="Input Image", width=400)

    pred = predict_class(np.asarray(test_image), model)

    class_names = ['Black Rot', 'Esca', 'Leaf Blight', 'Healthy']
    result = class_names[np.argmax(pred)]
    output = 'The Leaf is ' + result
    st.success(output)

    treatment = get_treatment_recommendation(result)
    st.info('Treatment Recommendation:')
    st.write(treatment)
