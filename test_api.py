import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy


from app import create_app
from models import  setup_db, db, Actor, Movie, Link # db_create_all_if_table_doesnt_exist,

# Change the following tokens as required
exec_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRpOGExamZlMVY3VWgwQVBTZmN6OCJ9.eyJpc3MiOiJodHRwczovL2Rldm9wc2tpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYjVhM2E5MGJkNGMyMDA2OGY2MTQ5MCIsImF1ZCI6Im1vdmlldGVzdCIsImlhdCI6MTYwNjU0ODA3NiwiZXhwIjoxNjA2NTU1Mjc2LCJhenAiOiJmOHp2NkdRZHllMXYxWTBNeWNvZG9iMG05VDJKWUdHbiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9yIiwiYWRkOm1vdmllIiwiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZWRpdDphY3RvciIsImVkaXQ6bW92aWUiLCJsaW5rOmNhc3RzIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.D6k_Fb5wCwUovDjjVUVZp71msKHuwYaOupW4XPA37JQB6J8G7oYJNknMzl3QvCdcQz9p69A-9HdiQrzCgWwsu7BxdQ-msjGIdfConNvpYNCPeOP3CNkUMRyIYtzFcD3AnzaVMGbtq8rq44LUlMGfgmD5XN7eO4ylxoXe80ObzNuiIUsnaOUfXMECYg1nPoLcvP5RmdstiMKa_CE56IprTAsSWZ7LDx9ih_Ao4m95P1ohffXTEEeBMYQ-rHpWmPj1F_2vLyMJdk8HyHU9PaapNJ-A_OYVTjhUzse9j4q86xwtRYvUUwr3KwuHMxyCbBq9P3rtVSyDnlWljxNgRGpRgg'
dir_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRpOGExamZlMVY3VWgwQVBTZmN6OCJ9.eyJpc3MiOiJodHRwczovL2Rldm9wc2tpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYjVhMzRlYTJkN2YzMDA2ZTZkYTEwMiIsImF1ZCI6Im1vdmlldGVzdCIsImlhdCI6MTYwNjU0Nzg3MywiZXhwIjoxNjA2NTU1MDczLCJhenAiOiJmOHp2NkdRZHllMXYxWTBNeWNvZG9iMG05VDJKWUdHbiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9yIiwiZGVsZXRlOmFjdG9yIiwiZWRpdDphY3RvciIsImVkaXQ6bW92aWUiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.t8gRKjzqvi1XAZb35_Uvx5gllbEgVOv5sKGTLyIvSTeo29MsPgm7N6gk3W90B5HsZ8BlFl_ypxFO7rFFvpV0_COXuCoWmcXu9ziBOrInlCW7JuhxR0QzUlZn4BOIBDRIYseh9ovZ7JpbTLyL5zd6CaggD1u1POrKMNYvau1iBzPTvxiorFE-9ntKkPi5Gy7uYTsG6HOaK3uxNLCLUPI5PtIQt2x4ZKj9Y97GYQit8h1b_xKZJsxnBJ8ZWC3akvmL09mBBETMk1UL4DLCJQbXBVUSp_d1smN7nzmrkFepj1xeJKNoDNr8UyE0bpBFTCNkjMiqZpy4oBTvERfwikrA1Q'
asst_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRpOGExamZlMVY3VWgwQVBTZmN6OCJ9.eyJpc3MiOiJodHRwczovL2Rldm9wc2tpbmcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYzFkM2Q4YzNjNmYwMDA3NTgxY2I2MCIsImF1ZCI6Im1vdmlldGVzdCIsImlhdCI6MTYwNjU0ODE2OCwiZXhwIjoxNjA2NTU1MzY4LCJhenAiOiJmOHp2NkdRZHllMXYxWTBNeWNvZG9iMG05VDJKWUdHbiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.GJZ7u4ByDO6Z814zvpn6HwAswKYzTuiaoL2_Yei_HRcZRf7Iqq_3RrI6XDs4MSEaZQ_R8QUrrsS1jc_5Y99vFwveSZbGE-nLr3HbDOkXB3EeBuS0Y-FkXAKcqiDUKkHzGDKLJCrHZ4RoRMzWauOjALYy6xFBI-ChZsX_qdnE5BlU3PcWzX-qaDWeF8Hh0Pru3D3YtAl4qUjR4j6T0BcEEfrQ8gCmfjO0sGi5t4K0i0T5yN62BtfITSrp7357v6uszthH5ovlqDYxirYb2vyhbqT1owwrswY3re9ceJZlmhzAk3BiUQeeutPHRVdRBYjG8i1DYOuvgBIXPE7hWd9hEg'



class CastingTestCase(unittest.TestCase):


    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client

        self.database_filename = "casting_test.db"
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.database_path = "sqlite:///{}".format(os.path.join(self.project_dir, self.database_filename))

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


    # TEST 1: TEST ACCESS TO ADD ACTORS WITHOUT AUTH
    def test_01_add_actor_no_auth(self):
        response = self.client().post('/actors', json=self.add_actor)
        data = response.json
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected')

    # TEST 2: TEST ACCESS TO ADD ACTORS WITH insufficient PERMISSION (AS CAST ASSISTANT)
    def test_02_add_actor_no_perm(self):
        response = self.client().post('/actors', json=self.add_actor, headers=self.headers_asst)
        data = response.json
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission Not found')

    # TEST 3: TEST ACCESS TO ADD ACTORS WITH SUFFICIENT PERMISSION (AS CAST DIRECTOR)
    def test_03_add_actor_with_perm(self):
        response = self.client().post('/actors', json=self.add_actor, headers=self.headers_dir)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_actor'], 'Kiki Nkunku')

    # TEST 4: TEST ACCESS TO VIEW ACTORS WITHOUT AUTH
    def test_04_view_actors_no_auth(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected')

    # TEST 5: TEST ACCESS TO VIEW ACTORS WITH SUFFICIENT PERMISSION (AS CAST ASSISTANT)
    def test_05_view_actors_with_perm(self):
        res = self.client().get('/actors', headers=self.headers_asst)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data['actors'][0]['__name'], 'Kiki Nkunku')

    # TEST 6: TEST ACCESS TO ADD MOVIES WITH INSUFFICIENT PERMISSION (AS CAST DIRECTOR)
    def test_06_add_movie_no_perm(self):
        response = self.client().post('/movies', json=self.add_movie , headers=self.headers_dir)
        data = response.json
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission Not found')

    # TEST 7: TEST ACCESS TO ADD MOVIES WITH SUFFICIENT PERMISSION (AS EXECUTIVE PRODUCER)
    def test_07_add_movie_with_perm(self):
        response = self.client().post('/movies', json=self.add_movie , headers=self.headers_exec)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_movie'], 'Malukani Junbulukeni')

    # TEST 8: TEST ACCESS TO VIEW MOVIES
    def test_08_view_movies(self):
      res = self.client().get('/movies', headers=self.headers_dir)
      data = json.loads(res.data)
      self.assertEqual(res.status_code, 200)
      self.assertEqual(data["success"], True)
      self.assertEqual(data['movies'][0]['__title'], 'Malukani Junbulukeni')

    # TEST 9: TEST ACCESS TO LINK MOVIES TO ACTORS (AS EXECUTIVE PRODUCER)
    def test_09_actor_movie_link(self):
        response = self.client().post('/link', json=self.add_link, headers=self.headers_exec)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['linked_actor'], 'Kiki Nkunku')
        self.assertEqual(data['linked_movie'], 'Malukani Junbulukeni')

    # TEST 10: TEST ACCESS TO EDIT ACTOR (AS CAST DIRECTOR)
    def test_10_edit_actor(self):
        response = self.client().patch('/actors/1', json=self.edit_actor, headers=self.headers_dir)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_name'], 'PATCHED Kiki Nkunku')

    # TEST 11: TEST ACCESS TO EDIT MOVIE (AS CAST DIRECTOR)
    def test_11_edit_movie(self):
        response = self.client().patch('/movies/1', json=self.edit_movie, headers=self.headers_dir)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_movie_title'], 'PATCHED Malukani Junbulukeni')

    # TEST 12: TEST ACCESS TO DELETE ACTOR (AS CAST DIRECTOR) [WITH PERMISSION]
    def test_12_delete_actor_with_perm(self):
        response = self.client().delete('/actors/1', headers=self.headers_dir)
        data = response.json
        actor = Actor.query.filter(Actor.id == 2).one_or_none()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_actor'], 'PATCHED Kiki Nkunku')
        self.assertEqual(actor, None)

    # TEST 13: TEST ACCESS TO DELETE MOVIE (AS CAST DIRECTOR) [NO PERMISSION]
    def test_13_delete_movie_no_perm(self):
        response = self.client().delete('/movies/1', headers=self.headers_dir)
        data = response.json
        actor = Movie.query.filter(Movie.id == 1).one_or_none()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission Not found')

    # TEST 14: TEST ACCESS TO DELETE MOVIE (AS EXECUTIVE PRODUCER) [with PERMISSION]
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