# services/supabase_service.py

from supabase import create_client, Client


class SupabaseClient:
    def __init__(self, url, key, table_name):
        if not url or not key:
            raise ValueError("Supabase URL and Key must be provided.")

        self.client: Client = create_client(url, key)
        self.table_name = table_name

    def insert_random_name(self, random_name):
        data = {'name': random_name}
        try:
            response = self.client.table(self.table_name).insert(data).execute()
            print(f"Inserted data into '{self.table_name}': {response.data}")
            return True
        except Exception as e:
            print(f"Error inserting data into '{self.table_name}': {e}")
            return False

    def get_table_count(self):
        try:
            response = self.client.table(self.table_name).select('*', count='exact').execute()
            if response.count is not None:
                return response.count
            else:
                print(f"Could not retrieve count from '{self.table_name}'.")
                return None
        except Exception as e:
            print(f"Error counting data in '{self.table_name}': {e}")
            return None

    def delete_oldest_entry(self):
        try:
            # Fetch all IDs from the table ordered by load_datetime
            response = self.client.table(self.table_name).select('id, load_datetime').order('load_datetime').limit(1).execute()
            if response.data:
                oldest_id = response.data[0]['id']
                oldest_load_datetime = response.data[0]['load_datetime']
                if not oldest_id:
                    print(f"No entries to delete in '{self.table_name}'.")
                    return True  # No deletion needed, but not an error
                
                # Delete entry with oldest load_datetime
                self.client.table(self.table_name).delete().eq('id', oldest_id).execute()
                print(f"Deleted oldest record with id {oldest_id} loaded {oldest_load_datetime} from '{self.table_name}'.")
                return True
            else:
                print(f"No data retrieved from '{self.table_name}'.")
                return False
        except Exception as e:
            print(f"Error deleting data from '{self.table_name}': {e}")
            return False
