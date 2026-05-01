from ._base import DataFrameFromJSONMixin
import pandas as pd 

def get_patientid(subject):
    '''
    Helper function to get a patient id from a FHIR reference string. 
    '''
    split_string = subject['reference'].split('/')
    return split_string[-1]

class Label(DataFrameFromJSONMixin):
    
    def __init__(self, path, patient_path):
        super().__init__(path)
        self.patient_df = pd.read_json(patient_path, lines = True)

    def get_stroke_ind(self, obs_df: pd.DataFrame, patient_df: pd.DataFrame):
        '''
        Create Stroke Indicator Column
        
        Args:
            obs_df: Observations DataFrame
            patient_df: Patient DataFrame
            
        Returns:
            pd.DataFrame: DataFrame with patient IDs and stroke indicators
        '''
     
        patient_df = patient_df[['id']]
        
        # Extract patient IDs from subject references
        obs_df['patientId'] = obs_df['subject'].apply(lambda x: get_patientid(x))
        
        # Create mapping for stroke vs no stroke
        stroke_mapping = {'Stroke': 1.0, 'noStroke': 0.0}
        
        # Filter observations that have valueCodeableConcept (stroke indicators)
        observations_df_stroke = obs_df[obs_df['valueCodeableConcept'].notnull()]
        
        # Extract text from valueCodeableConcept
        observations_df_stroke['valueCodeableConceptText'] = observations_df_stroke['valueCodeableConcept'].apply(lambda x: x['text'])
        
        # Filter for stroke observations only
        observations_df_stroke = observations_df_stroke[observations_df_stroke['valueCodeableConceptText'] == 'Stroke']
        observations_df_stroke['id'] = observations_df_stroke['patientId']
        
        # Merge with all patients
        stroke_df = patient_df.merge(observations_df_stroke, how='left', on='id')
        
        # Create stroke indicator column
        stroke_df['stroke_ind'] = stroke_df['valueCodeableConceptText'].replace(stroke_mapping)
        
        # Fill missing values with 0.0 (no stroke)
        stroke_df['stroke_ind'] = stroke_df['stroke_ind'].fillna(0.0)
        
        return stroke_df[['id', 'stroke_ind']]

    def pipeline(self):
        """
        Complete pipeline for creating stroke labels.
        """
        observation_df = self.data
        patient_df = self.patient_df 
        stroke_df = self.get_stroke_ind(observation_df, patient_df)
        return stroke_df