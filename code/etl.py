import pandas as pd
import streamlit as st 


def top_locations(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    location_amounts_df = violations_df.pivot_table(index = 'location', values = 'amount', aggfunc= 'sum').sort_values('amount', ascending= False)
    location_amounts_df['location'] = location_amounts_df.index
    location_amounts_df.reset_index(drop = True, inplace = True)
    return location_amounts_df[location_amounts_df['amount'] >= threshold]


def top_locations_mappable(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    top_locations_df = top_locations(violations_df, threshold)
    violations_filtered_df = violations_df[['location', 'lat', 'lon']].drop_duplicates(subset = ['location'])
    merged_df = pd.merge(top_locations_df, violations_filtered_df, on= 'location')
    return merged_df.drop_duplicates()


def tickets_in_top_locations(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    top_locations_df = top_locations(violations_df)
    merged_df = pd.merge(top_locations_df[['location']], violations_df, on = 'location')
    return merged_df

if __name__ == '__main__':
    '''
    Main ETL job. 
    '''
    # input original ticket file
    violations_df = pd.read_csv('./cache/final_cuse_parking_violations.csv')

    # make new dataframes
    top_locations_df = top_locations(violations_df)
    top_locations_mappable_df = top_locations_mappable(violations_df)
    tickets_in_top_locations_df = tickets_in_top_locations(violations_df)

    # save dataframes to csv
    top_locations_df.to_csv('./cache/top_locations.csv')
    top_locations_mappable_df.to_csv('./cache/top_locations_mappable.csv')
    tickets_in_top_locations_df.to_csv('./cache/tickets_in_top_locations.csv')