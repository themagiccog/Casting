import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy


from app import create_app
from models import  setup_db, db, Actor, Movie, Link # db_create_all_if_table_doesnt_exist,

# Change the following tokens as required
exec_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRpOGExamZlMVY3VWgwQVBTZmN6OCJ9.eyJpc3MiOiJodHRwczovL2Rldm9wc2tpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYjVhM2E5MGJkNGMyMDA2OGY2MTQ5MCIsImF1ZCI6Im1vdmlldGVzdCIsImlhdCI6MTYwNjU5MTAyMywiZXhwIjoxNjA2Njc3NDIzLCJhenAiOiJmOHp2NkdRZHllMXYxWTBNeWNvZG9iMG05VDJKWUdHbiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9yIiwiYWRkOm1vdmllIiwiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZWRpdDphY3RvciIsImVkaXQ6bW92aWUiLCJsaW5rOmNhc3RzIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.aI_1BlV8e1T8qKAAOtpAgD80JHOdsqIe1zsYbKXZ0U5LldB0C3NPJiujYO0KNkPVyrSfTGNBX00z5OJ3NBB9dW5usoX1Sw7XLiBCQ6Tv8Tznr18by2PyfkthOMHoPTF2bTWj01mtfnSiJWzPpKbLx00Gx8pkiBpFUKtX3KeAWZuVGKRx-mjTXOuuGkAZcpwkHPoumJOa-BAI9d0lkoqHTXQpjGVb6rOH_Bx245TldykQtiqqmSnMwMMPcBWosJouoB8vGXYmQgEFkslUJVPKSv87DaYhIvNpS1ZmlXsEMcXPw3jpgIUvSvpswiiGum6TzJRcURw1d-mrHGTH92s27A'
dir_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRpOGExamZlMVY3VWgwQVBTZmN6OCJ9.eyJpc3MiOiJodHRwczovL2Rldm9wc2tpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYjVhMzRlYTJkN2YzMDA2ZTZkYTEwMiIsImF1ZCI6Im1vdmlldGVzdCIsImlhdCI6MTYwNjU5MTExMCwiZXhwIjoxNjA2Njc3NTEwLCJhenAiOiJmOHp2NkdRZHllMXYxWTBNeWNvZG9iMG05VDJKWUdHbiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9yIiwiZGVsZXRlOmFjdG9yIiwiZWRpdDphY3RvciIsImVkaXQ6bW92aWUiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.MoM3BL6OgiiuLIUbUlBxqZtTR6EGgvaqqUH2RPDNZuKHCFBCQo6pXkW56vGHNzjoZCWO8skEEDfq3cpnuayk4ULvfEOT9RNiF3MTWebe9zDoXLGkVtVZwCzZ-AxHwdQG53129TIs-rXYB1_8dja-jtu9yGRnZoiZv_6wOuQ3Uzr1iluMvMO4dyZDxLRFio0FIrb16ewYAc_aPYSPm5SsJypW5xJcxJK5bRv9TWHUcJ0USnLY0pKlBMhWpF2ZCKmZKxA9iOZu_mwt_F8_3FHbKPq60mqx8zw4Bv3jQenOQ-JtbMRP1uYc0NnEQvOApU8l_yNIraOSuJGVs0bRBJY7Ew'
asst_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRpOGExamZlMVY3VWgwQVBTZmN6OCJ9.eyJpc3MiOiJodHRwczovL2Rldm9wc2tpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYzFkM2Q4YzNjNmYwMDA3NTgxY2I2MCIsImF1ZCI6Im1vdmlldGVzdCIsImlhdCI6MTYwNjU5MTE4NiwiZXhwIjoxNjA2Njc3NTg2LCJhenAiOiJmOHp2NkdRZHllMXYxWTBNeWNvZG9iMG05VDJKWUdHbiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.GFAM_qBoeoIG83ZE5K2D0Tr4p19e3NoXwt_0omST78VPZx5wQ91MdSN1qMjvD_zxlZcbeYY-kvxoY9aV8UP8C6RQ7WMxW3FtepFRS7bNIw0tkc_d2Sba38cZzQ7E5bFhMgByZJvaimWuyGwev9FKjJu5Hpyuo1MJkOVbtIydtyzbJW4rspreuIXUFolIAWbpLOjVCi88QGdV153lPuI5OqFPRqlOfnp4F9ENNq-PPfd0EyHlrUVDgoDt6cT9GtS4CqJgKCxEH0J8c7aKeJY0u4qXZ2OFAtHYYgWbUtz0k6hE4kBWJ1W8R-u3qAggIPGGkL69Vw09UHZm6nwf7azuuA'



class CastingTestCase(unittest.TestCase):


    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client

        # SQLite3 Config
        self.database_filename = "casting_test.db"
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        #self.database_path = "sqlite:///{}".format(os.path.join(self.project_dir, self.database_filename))

        
        # Postgres Config
        self.database_name = "casting_test"
        self.user = "cog"
        self.passwd = "1234"
        self.database_path = "postgres://{}:{}@{}/{}".format(self.user, self.passwd,'localhost:5432', self.database_name)
        
        self.headers_asst = {'Content-Type': 'application/json',
                                  'Authorization': asst_token}
        self.headers_dir = {'Content-Type': 'application/json',
                                 'Authorization': dir_token}
        self.headers_exec = {'Content-Type': 'application/json',
                                 'Authorization': exec_token}


        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            #self.db.create_all()


        self.add_actor = {"name": "Kiki Nkunku",
                          "age": 25,
                          "gender": "Female"}
        self.edit_actor = {"name": "PATCHED Kiki Nkunku",
                          "age": 99,
                          "gender": "Male"}
        self.add_link = {
                          "movie_id": 1,
                          "actor_id": 1
                        }
        self.add_movie = {
                            "title": "Malukani Junbulukeni",
                            "releasedate": 1983
                          }
        self.edit_movie = {
                            "title": "PATCHED Malukani Junbulukeni",
                            "releasedate": 9999
                          }

    def tearDown(self):
        """Executed after each test"""
        pass


    # # TEST 1: TEST ACCESS TO ADD ACTORS WITHOUT AUTH
    def test_01_add_actor_no_auth(self):
        response = self.client().post('/actors', json=self.add_actor)
        data = response.json
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected')

    # # TEST 2: TEST ACCESS TO ADD ACTORS WITH insufficient PERMISSION (AS CAST ASSISTANT)
    def test_02_add_actor_no_perm(self):
        response = self.client().post('/actors', json=self.add_actor, headers=self.headers_asst)
        data = response.json
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission Not found')

    # # TEST 3: TEST ACCESS TO ADD ACTORS WITH SUFFICIENT PERMISSION (AS CAST DIRECTOR)
    def test_03_add_actor_with_perm(self):
        response = self.client().post('/actors', json=self.add_actor, headers=self.headers_dir)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_actor'], 'Kiki Nkunku')

    # # TEST 4: TEST ACCESS TO VIEW ACTORS WITHOUT AUTH
    def test_04_view_actors_no_auth(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected')

    # # TEST 5: TEST ACCESS TO VIEW ACTORS WITH SUFFICIENT PERMISSION (AS CAST ASSISTANT)
    def test_05_view_actors_with_perm(self):
        res = self.client().get('/actors', headers=self.headers_asst)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data['actors'][0]['__name'], 'Kiki Nkunku')

    # # TEST 6: TEST ACCESS TO ADD MOVIES WITH INSUFFICIENT PERMISSION (AS CAST DIRECTOR)
    def test_06_add_movie_no_perm(self):
        response = self.client().post('/movies', json=self.add_movie , headers=self.headers_dir)
        data = response.json
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission Not found')

    # # TEST 7: TEST ACCESS TO ADD MOVIES WITH SUFFICIENT PERMISSION (AS EXECUTIVE PRODUCER)
    def test_07_add_movie_with_perm(self):
        response = self.client().post('/movies', json=self.add_movie , headers=self.headers_exec)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_movie'], 'Malukani Junbulukeni')

    # # TEST 8: TEST ACCESS TO VIEW MOVIES
    def test_08_view_movies(self):
      res = self.client().get('/movies', headers=self.headers_dir)
      data = json.loads(res.data)
      self.assertEqual(res.status_code, 200)
      self.assertEqual(data["success"], True)
      self.assertEqual(data['movies'][0]['__title'], 'Malukani Junbulukeni')

    # # TEST 9: TEST ACCESS TO LINK MOVIES TO ACTORS (AS EXECUTIVE PRODUCER)
    def test_09_actor_movie_link(self):
        response = self.client().post('/link', json=self.add_link, headers=self.headers_exec)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['linked_actor'], 'Kiki Nkunku')
        self.assertEqual(data['linked_movie'], 'Malukani Junbulukeni')

    # # TEST 10: TEST ACCESS TO EDIT ACTOR (AS CAST DIRECTOR)
    def test_10_edit_actor(self):
        response = self.client().patch('/actors/1', json=self.edit_actor, headers=self.headers_dir)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_name'], 'PATCHED Kiki Nkunku')

    # # TEST 11: TEST ACCESS TO EDIT MOVIE (AS CAST DIRECTOR)
    def test_11_edit_movie(self):
        response = self.client().patch('/movies/1', json=self.edit_movie, headers=self.headers_dir)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_movie_title'], 'PATCHED Malukani Junbulukeni')

    # # TEST 12: TEST ACCESS TO DELETE ACTOR (AS CAST DIRECTOR) [WITH PERMISSION]
    def test_12_delete_actor_with_perm(self):
        response = self.client().delete('/actors/1', headers=self.headers_dir)
        data = response.json
        actor = Actor.query.filter(Actor.id == 2).one_or_none()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_actor'], 'PATCHED Kiki Nkunku')
        self.assertEqual(actor, None)

    # # TEST 13: TEST ACCESS TO DELETE MOVIE (AS CAST DIRECTOR) [NO PERMISSION]
    def test_13_delete_movie_no_perm(self):
        response = self.client().delete('/movies/1', headers=self.headers_dir)
        data = response.json
        actor = Movie.query.filter(Movie.id == 1).one_or_none()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission Not found')

    # # TEST 14: TEST ACCESS TO DELETE MOVIE (AS EXECUTIVE PRODUCER) [with PERMISSION]
    def test_13_delete_movie_no_perm(self):
      response = self.client().delete('/movies/1', headers=self.headers_exec)
      data = response.json
      actor = Movie.query.filter(Movie.id == 1).one_or_none()
      self.assertEqual(response.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertEqual(data['deleted_movie'], 'PATCHED Malukani Junbulukeni')
      self.assertEqual(actor, None)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()