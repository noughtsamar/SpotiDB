from datetime import date
import streamlit as st
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Murakami@29",
    database="spotifydb"
)
cursor = db.cursor()


def login_history_page():
    st.title('Login History')

    # Get date input from the user
    selected_date = st.date_input('Select Date', date.today())
    selected_date_str = selected_date.strftime("%Y-%m-%d")

    # Fetch login count for the selected date
    query_login_count = "SELECT * FROM login_count WHERE LoginDate = %s"
    cursor.execute(query_login_count, (selected_date,))
    login_data = cursor.fetchone()

    if login_data:
        st.write(f"Date: {selected_date}")
        st.write(f"Total Logins: {login_data[1]}")
    else:
        st.warning(f"No login data available for {selected_date}")

def increment_total_login_count():
    # Get the current date
    current_date = date.today()

    # Check if there is already a record for the current date
    query_check = "SELECT Count FROM login_count WHERE LoginDate = %s"
    cursor.execute(query_check, (current_date,))
    existing_count = cursor.fetchone()

    if existing_count:
        # If a record exists, increment the count
        count = existing_count[0] + 1
        query_update = "UPDATE login_count SET Count = %s WHERE LoginDate = %s"
        cursor.execute(query_update, (count, current_date))
    else:
        # If no record exists, insert a new record with count 1
        query_insert = "INSERT INTO login_count (LoginDate, Count) VALUES (%s, %s)"
        cursor.execute(query_insert, (current_date, 1))

    # Commit the changes to the database
    db.commit()


def get_total_login_count():
    # Get the current date
    current_date = date.today()

    # Check if there is a record for the current date
    query_check = "SELECT Count FROM login_count WHERE LoginDate = %s"
    cursor.execute(query_check, (current_date,))
    existing_count = cursor.fetchone()

    return existing_count[0] if existing_count else 0
def admin_register(email, password, user_id, dob, username, role='admin'):
    query = "INSERT INTO useraccount (Email, UserPassword, UserID, Dob, UserName, UserRole) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (email, password, user_id, dob, username, role)
    cursor.execute(query, values)
    db.commit()

def admin_register_page():
    st.title('Admin Registration')

    admin_email = st.text_input('Admin Email', key='admin_email')
    admin_password = st.text_input(
        'Admin Password', type='password', key='admin_password')
    admin_user_id = st.number_input(
        'Admin User ID', min_value=1, key='admin_user_id')
    admin_dob = st.date_input('Admin Date of Birth', key='admin_dob')
    admin_username = st.text_input('Admin Username', key='admin_username')

    admin_register_button = st.button(
        'Register as Admin', key='admin_register_button')

    if admin_register_button:
        admin_register(admin_email, admin_password,
                       admin_user_id, admin_dob, admin_username)
        st.success('Admin registered successfully')

def get_user_details(email, password):
    query = "SELECT UserID, UserName, UserRole FROM useraccount WHERE Email = %s AND UserPassword = %s"
    cursor.execute(query, (email, password))
    result = cursor.fetchone()
    return result if result else None


def register_user_procedure(email, password, user_id, dob, username, role='user'):
    query = "CALL RegisterUser(%s, %s, %s, %s, %s, %s)"
    values = (email, password, user_id, dob, username, role)
    cursor.execute(query, values)
    db.commit()


def register_user(email, password, user_id, dob, username, role='user'):
    register_user_procedure(email, password, user_id, dob, username, role)


def register_user_page():
    st.title('User Registration')

    user_email = st.text_input('User Email', key='user_email')
    user_password = st.text_input(
        'User Password', type='password', key='user_password')
    user_user_id = st.number_input(
        'User ID', min_value=1, key='user_user_id')
    user_dob = st.date_input('User Date of Birth', key='user_dob')
    user_username = st.text_input('User Username', key='user_username')

    register_user_button = st.button(
        'Register as User', key='register_user_button')

    if register_user_button:
        register_user(user_email, user_password,
                      user_user_id, user_dob, user_username)
        st.success('User registered successfully')


def logregpage():
    login_form_state = st.session_state.get('login_form_state', False)
    register_form_state = st.session_state.get('register_form_state', False)

    # Streamlit UI
    st.title('User Authentication')

    if st.button('Login', key='login_button'):
        login_form_state = True
        register_form_state = False

    if st.button('Register', key='register_button'):
        register_form_state = True
        login_form_state = False

    if login_form_state:
        st.session_state.login_form_state = True
        st.header('Login')
        login_email = st.text_input('Email', key='login_email')
        login_password = st.text_input(
            'Password', type='password', key='login_password')
        login_button = st.button('Login', key='login_submit')

        if login_button:
            user_data = get_user_details(login_email, login_password)
            if user_data:
                user_id, username, user_role = user_data
                st.session_state.username = username
                st.session_state.user_id = user_id
                st.session_state.user_role = user_role
                st.success(f'Login successful! Hello, {username}')
                st.session_state.user_data_page_state = True

     
                increment_total_login_count()
            else:
                st.error('Incorrect email or password')

    if register_form_state:
        st.session_state.register_form_state = True
        st.header('Register')
        register_email = st.text_input('Email', key='register_email')
        register_password = st.text_input(
            'Password', type='password', key='register_password')
        register_user_id = st.number_input(
            'User ID', min_value=1, key='register_user_id')
        register_dob = st.date_input('Date of Birth', key='register_dob')
        register_username = st.text_input('Username', key='register_username')
        register_button = st.button('Register', key='register_submit')

        if register_button:
            register_user(register_email, register_password,
                          register_user_id, register_dob, register_username)
            st.success('User registered successfully')


def admin_page():
    # Check if the logged-in user is an admin
    if st.session_state.get('user_role') == 'admin':
        # Display admin-specific content here
        st.write("Admin Page")
    elif st.session_state.get('user_role') == 'user':
        st.warning("You don't have permission to access this page.")

def album():
    username = st.session_state.get('username', None)
    user_id = st.session_state.get('user_id', None)
    user_role = st.session_state.get('user_role', 'user')

    if user_role == 'admin':
        st.header("Admin View: All Albums")
        query = "SELECT * FROM album"
        cursor.execute(query)
        albums = cursor.fetchall()
        st.write("---------------")
        for album_data in albums:
            st.write(f"Album Name: {album_data[1]}")
            st.write(f"Release Date: {album_data[2]}")
            st.write(f"Album Type: {album_data[3]}")
            st.write(f"Artist Name: {album_data[4]}")
            st.write("---------------")
    elif username and user_id:
        st.header(f"{username}'s Albums:")

        query = "SELECT * FROM album WHERE UserID = %s"
        cursor.execute(query, (user_id,))
        albums = cursor.fetchall()
        st.write("---------------")
        for album_data in albums:
            st.write(f"Album Name: {album_data[1]}")
            st.write(f"Release Date: {album_data[2]}")
            st.write(f"Album Type: {album_data[3]}")
            st.write(f"Artist Name: {album_data[4]}")
            st.write("---------------")
    else:
        st.warning("Please log in to access your data.")


def create_album(aid, album_name, release_date, album_type, artist_name, user_id):
    query = "INSERT INTO album (AlbumID, AlbumName, ReleaseDate, Album_Type, ArtistName, UserID) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (aid, album_name, release_date, album_type, artist_name, user_id)
    cursor.execute(query, values)
    db.commit()


def create_album_page():
    st.title('Create Album')

    user_id = st.session_state.get('user_id', None)
    if not user_id:
        st.warning("Please log in to create an album.")
        return

    #album_id = st.number_input('Album ID', key='create_album_name')
    aid = st.number_input("Album ID", min_value=1,
                          max_value=100, step=1, key='create_album_id')
    album_name = st.text_input('Album Name', key='create_album_name')
    release_date = st.date_input('Release Date', key='create_release_date')
    album_type = st.text_input('Album Type', key='create_album_type')
    artist_name = st.text_input('Artist Name', key='create_artist_name')

    create_album_button = st.button('Create Album', key='create_album_button')

    if create_album_button:
        create_album(aid, album_name, release_date, album_type, artist_name, user_id)
        st.success('Album created successfully')


### Delete Operation for Albums

def delete_album(album_id):
    query = "DELETE FROM album WHERE AlbumID = %s"
    cursor.execute(query, (album_id,))
    db.commit()


def delete_album_page():
    st.title('Delete Album')

    user_id = st.session_state.get('user_id', None)
    if not user_id:
        st.warning("Please log in to delete an album.")
        return

    # Fetch user's albums
    query = "SELECT AlbumID, AlbumName FROM album WHERE UserID = %s"
    cursor.execute(query, (user_id,))
    albums = cursor.fetchall()

    if not albums:
        st.warning("You don't have any albums to delete.")
        return

    selected_album_id = st.selectbox('Select Album to Delete', [
                                     f"{album[1]} (ID: {album[0]})" for album in albums], key='delete_album_select')

    album_id = int(selected_album_id.split('(ID: ')[1][:-1])

    delete_album_button = st.button('Delete Album', key='delete_album_button')

    if delete_album_button:
        delete_album(album_id)
        st.success('Album deleted successfully')

def artist():
    username = st.session_state.get('username', None)
    user_id = st.session_state.get('user_id', None)
    user_role = st.session_state.get('user_role', 'user')

    if user_role == 'admin':
        st.header("Admin View: All Artists")
        query = "SELECT * FROM artist"
        cursor.execute(query)
        artists = cursor.fetchall()

        st.write("---------------")
        for artist_data in artists:
            st.write(f"Artist ID: {artist_data[0]}")
            st.write(f"Artist Name: {artist_data[1]}")
            st.write("---------------")
    elif username and user_id:
        st.header(f"{username}'s Artists:")

        query = "SELECT * FROM artist WHERE UserID = %s"
        cursor.execute(query, (user_id,))
        artists = cursor.fetchall()
        new_query = """
        SELECT s.SongID, s.SongName, s.ArtistID, s.Popularity, a.ArtistID
        FROM song s
        JOIN artist a ON s.ArtistID = a.ArtistID
        WHERE s.UserID = %s
        """
        cursor.execute(new_query, (user_id,))
        songs_for_user = cursor.fetchall()
        st.write("---------------")
       
        st.write("---------------")
        for artist_data in artists:
            st.write(f"Artist ID: {artist_data[0]}")
            st.write(f"Artist Name: {artist_data[1]}")
            st.write("---------------")


        st.header("Displaying The Song by the artists in the Database using Left Join")
        st.write("---------------")
        #print(songs_for_user)
        for artist_song in songs_for_user:
            st.write(f"SongID: {artist_song[0]}")
            st.write(f"Song Name: {artist_song[1]}")
            st.write(f"Artist Name: {artist_song[2]}")
            st.write(f"Popularity: {artist_song[3]}")
            st.write(f"Artist ID: {artist_song[4]}")
            st.write("---------------")
    else:
        st.warning("Please log in to access your data.")


def song_page():
    user_id = st.session_state.get('user_id', None)
    username = st.session_state.get('username', None)
    user_role = st.session_state.get('user_role', 'user')

    if user_role == 'admin':
        st.header("Admin View: All Songs")
        query = "SELECT * FROM song"
        cursor.execute(query)
        songs = cursor.fetchall()

        st.write("---------------")
        for song_data in songs:
            st.write(f"Track Name: {song_data[4]}")
            st.write(f"Artist: {song_data[1]}")
            st.write(f"Album Name: {song_data[2]}")
            st.write(f"Track Duration (ms): {song_data[5]}")
            st.write(f"Popularity: {song_data[3]}")
            st.write("---------------")
    elif user_id:
        st.header(f"{username}'s Songs:")

        # Fetch song data for the specific user
        query = "SELECT * FROM song WHERE UserID = %s"
        cursor.execute(query, (user_id,))
        songs = cursor.fetchall()

        st.write("---------------")
        for song_data in songs:
            st.write(f"Track Name: {song_data[4]}")
            st.write(f"Artist: {song_data[1]}")
            st.write(f"Album Name: {song_data[2]}")
            st.write(f"Track Duration (ms): {song_data[5]}")
            st.write(f"Popularity: {song_data[3]}")
            st.write("---------------")

        new_query = "SELECT * FROM song WHERE popularity = (SELECT MAX(popularity) FROM song WHERE UserID = %s)"
        cursor.execute(new_query, (user_id,))
        max_popularity_song = cursor.fetchone()

        st.write("---------------")
        st.write("Song with Maximum Popularity:")
        st.write(f"Track Name: {max_popularity_song[4]}")
        st.write(f"Artist: {max_popularity_song[1]}")
        st.write(f"Track ID: {max_popularity_song[2]}")
        st.write(f"Track Duration (ms): {max_popularity_song[5]}")
        st.write(f"Popularity: {max_popularity_song[3]}")
        st.write("---------------")
    else:
        st.warning("Please log in to access your data.")


def update_playlist(playlist_id, new_name):
    query = "UPDATE playlist SET PlaylistName = %s WHERE PlaylistID = %s"
    cursor.execute(query, (new_name, playlist_id))
    db.commit()


def playlist_page():
    username = st.session_state.get('username', None)
    user_id = st.session_state.get('user_id', None)
    user_role = st.session_state.get('user_role', 'user')

    if user_role == 'admin':
        st.header("Admin View: All Playlists")
        query = "SELECT * FROM playlist"
        cursor.execute(query)
        playlists = cursor.fetchall()

        for playlist_data in playlists:
            with st.form(f"update_form_{playlist_data[0]}"):
                st.write("---------------")
                st.write(f"Playlist ID: {playlist_data[0]}")
                st.write(f"Playlist Name: {playlist_data[2]}")
                st.write(f"Owner: {username}")
                st.write(f"Total Tracks: {playlist_data[3]}")

                # Add an update option for each playlist
                update_name = st.text_input(
                    f"Update Name for Playlist {playlist_data[0]}", key=f"update_name_{playlist_data[0]}")
                if st.form_submit_button(f"Update Playlist {playlist_data[0]}"):
                    update_playlist(playlist_data[0], update_name)
                    st.success(
                        f"Playlist {playlist_data[0]} updated successfully.")

                st.write("---------------")
    elif username and user_id:
        st.header(f"{username}'s Playlists:")

        # Fetch playlist data for the specific user
        query = "SELECT * FROM playlist WHERE UserID = %s"
        cursor.execute(query, (user_id,))
        playlists = cursor.fetchall()

        for playlist_data in playlists:
            with st.form(f"update_form_{playlist_data[0]}"):
                st.write("---------------")
                st.write(f"Playlist ID: {playlist_data[0]}")
                st.write(f"Playlist Name: {playlist_data[2]}")
                st.write(f"Owner: {username}")
                st.write(f"Total Tracks: {playlist_data[3]}")

                # Add an update option for each playlist
                update_name = st.text_input(
                    f"Update Name for Playlist {playlist_data[0]}", key=f"update_name_{playlist_data[0]}")
                if st.form_submit_button(f"Update Playlist {playlist_data[0]}"):
                    update_playlist(playlist_data[0], update_name)
                    st.success(
                        f"Playlist {playlist_data[0]} updated successfully.")

                st.write("---------------")
    else:
        st.warning("Please log in to access your data.")


# procedure
cursor.execute("DROP PROCEDURE IF EXISTS RegisterUser")
# Stored Procedure for User Registration
query_create_user_procedure = """
CREATE PROCEDURE RegisterUser(
  IN userEmail VARCHAR(255),
  IN userPassword VARCHAR(255),
  IN userUserID INT,
  IN userDOB DATE,
  IN userUsername VARCHAR(255),
  IN userRole VARCHAR(50)
)
BEGIN
  -- Add user to useraccount table
  INSERT INTO useraccount (Email, UserPassword, UserID, Dob, UserName, UserRole)
  VALUES (userEmail, userPassword, userUserID, userDOB, userUsername, userRole);
END
"""
cursor.execute(query_create_user_procedure, multi=True)
db.commit()





#admin account trigger
def admin_accounts_page():
    # Check if the logged-in user is an admin
    if st.session_state.get('user_role') == 'admin':
        st.header("Admin View: Admin Accounts")

        # Fetch all admin accounts
        query = "SELECT AdminUsername FROM adminaccount"
        cursor.execute(query)
        admins = cursor.fetchall()

        st.write("---------------")
        st.write("List of Admin Usernames:")
        for admin_data in admins:
            st.write(f"Admin Username: {admin_data[0]}")
            st.write("---------------")
    else:
        st.warning("You don't have permission to access this page.")


def user_accounts_page():
    # Check if the logged-in user is an admin
    if st.session_state.get('user_role') == 'admin':
        st.header("Admin View: User Accounts")

        # Fetch all user accounts
        query = "SELECT UserName FROM useraccount WHERE UserRole = 'user'"
        cursor.execute(query)
        users = cursor.fetchall()

        st.write("---------------")
        st.write("List of Usernames:")
        for user_data in users:
            st.write(f"Username: {user_data[0]}")
            st.write("---------------")
        max_popularity_query = """
        SELECT ua.UserID, ua.UserName, ua.UserRole
        FROM useraccount ua
        WHERE ua.UserID IN (
            SELECT f.UserID
            FROM follows f
            WHERE f.ArtistID IN (
                SELECT ar.ArtistID
                FROM album al
                JOIN artist ar ON al.ArtistName = ar.ArtistName
                WHERE al.ReleaseDate >= '2000-01-01'
            )
        );

        """
        cursor.execute(max_popularity_query)
        users_following_artists = cursor.fetchall()


        st.write("---------------")
        st.write("Users Following Artists with Albums Released After 2000-01-01:")
        st.write("---------------")

# Display each user's information
        for user_data in users_following_artists:
            st.write(f"User ID: {user_data[0]}")
            st.write(f"Username: {user_data[1]}")
            st.write(f"User Role: {user_data[2]}")
            st.write("---------------")

    else:
        st.warning("You don't have permission to access this page.")




page = st.sidebar.selectbox(
    'Select a Page', ('Login/Register', 'Albums', 'Artists', 'Songs', 'Playlists', 'Admin', 'Admin Accounts', 'User Accounts', 'Login History'))
if page == 'Login/Register':
    logregpage()
elif page == 'Albums':
    album()
    create_album_page()
    delete_album_page()
elif page == 'Songs':
    song_page()
elif page == 'Artists':
    artist()
elif page == 'Playlists':
    playlist_page()
elif page == 'Admin':
    admin_page()
    admin_register_page()
elif page == 'Admin Accounts':
    admin_accounts_page()
elif page == 'User Accounts':
    user_accounts_page()
elif page == 'Login History':
    login_history_page()

# Close the cursor and database connection
cursor.close()
db.close()
