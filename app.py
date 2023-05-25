import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import base64
from googletrans import Translator
from streamlit_option_menu import option_menu
import smtplib

st.set_page_config(layout="wide")

translator = Translator()
model = tf.keras.models.load_model('./grapes.h5')


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('1.jpg') 
st.set_option('deprecation.showfileUploaderEncoding', False)

def predict_class(image, model):
    image = tf.cast(image, tf.float32)
    image = tf.image.resize(image, [256, 256])
    image = np.expand_dims(image, axis=0)
    prediction = model.predict(image)
    return prediction

def get_treatment_recommendation(result):
    if result == 'Black Rot':
        return '''
        Identification :
        Black rot initially appears as small yellowish spots that enlarge and develop a dark border around the margins, 
        reddish-brown centers in the lesions, appearance of minute black dots (fungal fruiting bodies) containing summer spores, 
        oval-shaped and sunken lesions that are purple to black, lesions may also appear on young shoots, cluster stems, and tendrils. 
        In the later stages, small, light-brownish spots form on the fruit, which quickly enlarge, rot the entire berry, and result in 
        shriveled, black, and wrinkled fruit (mummies). Tiny black pycnidia may also form on the fruit mummies.

        Control : 
        1)Chemical Treatment:
         -  Fungicides: Various fungicides, such as Bordeaux mixture, Mancozeb, Topsin-M, 
            Ziram, and Captan, can be used to control leaf blight in grape leaves. 
            These fungicides should be applied according to their recommended dosage and 
            application frequency.
        2)Organic Treatment:
         -  Copper-based Sprays: Copper-based fungicides, such as copper sulfate or 
            copper hydroxide, can be used as organic alternatives to synthetic fungicides. 
            These sprays help prevent and control leaf blight in grape leaves.
         -  Neem Oil: Neem oil is a natural fungicide that can be effective against fungal 
            diseases, including leaf blight. It should be applied following the instructions 
            on the product label.
         -  Baking Soda Solution: A mixture of water and baking soda can be sprayed on grape 
            leaves affected by leaf blight. This solution creates an alkaline environment that 
            inhibits fungal growth.'''
        
    elif result == 'Esca':
        return '''Identification :
        1)Chlorosis: Leaves may exhibit yellowing or discoloration between the veins, giving a mottled appearance. This symptom is 
        commonly referred to as "Tiger stripe" or "Leaf yellowing."
        2)Necrosis: Browning or blackening of leaf tissue, typically starting from the leaf margin or leaf tip and progressing inward. 
        Necrotic areas may have a wedge or V-shaped pattern.
        3)Leaf Curling: Affected leaves may show upward or downward curling, distortion, or cupping.
        4)Leaf Size Reduction: Leaves may appear smaller in size than healthy leaves and may have irregular shape or lobes.
        5)Brown Veins: Discoloration or browning of the veins, often accompanied by reddish-brown streaks or spots along the veins.
        6)Wood Canker: Esca can cause wood decay and cankers in the trunk and arms of the grapevine. Look for black or brown discoloration 
        and sunken areas on the wood.

        Control :
        1)Chemical Treatment:
          - Fungicide sprays: Apply fungicides that are specifically labeled for the control of esca disease. 
            Follow the recommended application rates and timing provided by the manufacturer.
          - Systemic fungicides: Consider using systemic fungicides that can be absorbed by the plant and provide 
            long-lasting protection against the disease.
          - Protective fungicides: Apply protective fungicides before the onset of symptoms or during periods of
            high disease pressure to prevent infection.
            
        2)Organic Treatment:
         -  Trichoderma-based products: Use Trichoderma spp. biocontrol agents, which are
            beneficial fungi that can help suppress esca pathogens.
         -  Bacillus-based products: Apply Bacillus subtilis or other Bacillus species-based
            products, which are natural antagonists that can inhibit the growth of esca-causing fungi.
         -  Essential oils: Consider using essential oils such as clove, oregano, or thyme,
            which have antimicrobial properties and can help control fungal pathogens.
         -  Cultural practices: Implement cultural practices that promote plant health, such as proper 
            pruning techniques, maintaining good vineyard hygiene, and optimizing vine nutrition and irrigation.'''
            
    elif result == 'Leaf Blight':
        return '''
        Identification :
        Leaf blight in grape leaves is characterized by the appearance of small yellowish spots along the leaf margins, which gradually enlarge and turn 
        into brownish patches with concentric rings. Severe infections can lead to drying and defoliation of leaves. Additionally, dark brown-purplish 
        patches may appear on infected berries, rachis, and bunch stalks just below their attachment with the shoots. Proper identification of these 
        symptoms is important for timely intervention and disease management.
        
        Control : 
        1)Chemical Treatments:
         -  Bordeaux Mixture: A copper-based fungicide that helps control leaf blight in grapes.
         -  Mancozeb: A broad-spectrum fungicide effective against various fungal diseases, including leaf blight.
         -  Topsin-M: A systemic fungicide that provides control against leaf blight and other fungal infections.
         -  Ziram: A protective fungicide used to prevent and control leaf blight in grape leaves.
         -   Captan: A multi-purpose fungicide effective against leaf blight and other fungal diseases.

        2)Organic Treatments:
         -  Neem Oil: A natural fungicide with antifungal properties that can be used to control leaf blight.
         -  Bacillus subtilis: A beneficial bacteria-based product that suppresses fungal diseases, 
            including leaf blight.
         -  Serenade Garden Disease Control: A biological fungicide containing Bacillus subtilis that can be 
            applied to control leaf blight.
         -  Garlic Extract: Garlic has antifungal properties and can be used as a natural spray to help manage 
            leaf blight.
         -  Copper Soap: A copper-based organic fungicide that provides control against leaf blight and other 
            fungal infections.'''
    
    elif result == 'Healthy':
        st.balloons()
        return 'No treatment needed. The leaf is healthy.'
    else:
        return 'Unknown disease. Consult an expert for proper treatment.'

def translate_text(text, target_language):
    translation = translator.translate(text, dest=target_language)
    return translation.text


def send_text_message(contact_number, feedback_message): 
    # feedback_message = 
    st.success("Message sent successfully!")

EXAMPLE_NO = 1
def streamlit_menu(example=1):
    if example == 1:
        # 1. as sidebar menu
        with st.sidebar:
            selected = option_menu(
                menu_title="Main Menu",  # required
                options=["Home", "Disease Detector", "Contact"],  # required
                icons=["house", "book", "envelope"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
            )
        return selected

    if example == 2:
        # 2. horizontal menu w/o custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["Home", "Disease Detector", "Contact"],  # required
            icons=["house", "book", "envelope"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
        )
        return selected
    

    if example == 3:
        # 2. horizontal menu with custom style
        selected = option_menu(
            menu_title=None,  # required
            options=["Home", "Disease Detector", "Contact"],  # required
            icons=["house", "book", "envelope"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "25px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "green"},
            },
        )
        return selected
    
selected = streamlit_menu(example=EXAMPLE_NO)

if selected == "Home":
    st.title(f"{selected}")
    st.header("Welcome to Grape Leaf Disease Detector! ")
    st.subheader(f'''
    This web app helps identify common diseases in grape leaves and provides treatment recommendations.
    This web app is created using Streamlit, TensorFlow, PIL, base64, and googletrans libraries.
    It utilizes a deep learning model to classify grape leaf diseases.
    Upload an image of a grape leaf, and the model will predict the disease. 
    The corresponding treatment recommendation will be displayed.
    The app also includes translation functionality to translate the treatment recommendations into different languages.''')
if selected == "Disease Detector":
    st.title(f"{selected}")
    file = st.file_uploader("Upload an image of a leaf", type=["jpg", "png"])
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

        st.subheader('Translation')
        target_language = st.radio("Select target language:", ("English", "Marathi", "Hindi"))
        if target_language != "English":
            translated_treatment = translate_text(treatment, target_language.lower())
            st.write(f"Translated treatment ({target_language}):")
            st.write(translated_treatment)
if selected == "Contact":
    st.title(f"{selected}")
    contact_number = 0 
    st.header("Feedback Form")
    feedback_message = st.text_area("Message", height=200)
    if st.button("Send Message"):
        if feedback_message.strip() == "":
            st.warning("Please enter a feedback message.")
        else:
            send_text_message(contact_number, feedback_message)
    col1, col2 = st.columns(2)
    if col1.button("👍"):
        st.success("You liked the app, Thank you!")
    if col2.button("👎"):
        st.error("You disliked the app!")
