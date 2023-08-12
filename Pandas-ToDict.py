import pandas as pd

df = pd.DataFrame()

def Create_Data(df): 
    """
    This function takes a pandas DataFrame and converts each row into a dictionary,
    which is then used to create a contact data object.
    """

    try:
        
        data = []
        for i, row in df.iterrows():

            contact_data = {
                "id": "",
                "ListId": 'LIST_ID',
                "data": row.to_dict(),
                "callable": True
            }

            data.append(contact_data)

        return data

    except Exception as e:
        print(f"Error while Converting row in dict format :: {str(e)}")

Create_Data(df=df)