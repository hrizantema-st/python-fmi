import uuid
import datetime
from queue import Queue
MAX_SIZE_POST_QUEUE = 50


class User:
    def __init__(self, full_name):
        self.full_name = full_name
        self.uuid = uuid.uuid4()
        self.posts = Queue(maxsize=MAX_SIZE_POST_QUEUE)

    def __repr__(self):
        return "('{}' - '{}')".format(self.full_name, self.uuid)

    def __str__(self):
        return repr(self)

    def __hash__(self):
        return hash(self.__str__())

    def get_name(self):
        return self.full_name

    def get_uuid(self):
        return self.uuid

    def add_post(self, post_content):
        new_post = Post(post_content, self.uuid)
        if self.posts.full():
            self.posts.get()
        self.posts.put(new_post)

    def get_post(self):
        tmp_quee = Queue(maxsize=MAX_SIZE_POST_QUEUE)
        while not self.posts.empty():
            current_post = self.posts.get()
            tmp_quee.put(current_post)
            yield current_post
        self.posts = tmp_quee


class Post:
    def __init__(self, content, author):
        self.content = content
        self.published_at = datetime.datetime.now()
        self.author = author


class SocialGraph:

    def __init__(self):
        self._graph = {}

    def add_user(self, user):
        if user in self._graph.keys():
            raise UserAlreadyExistsError
        else:
            self._graph[user] = []

    def get_user_by_uuid(self, user_uuid):
        for user in self._graph.keys():
            if user_uuid == user.get_uuid():
                return user
        raise UserDoesNotExistError

    def does_user_exist(self, user_uuid):
        list_uuid = [u.get_uuid() for u in self._graph.keys()]
        return user_uuid in list_uuid

    def get_user(self, user_uuid):
        if self.does_user_exist(user_uuid):
            return self.get_user_by_uuid(user_uuid)
        else:
            raise UserDoesNotExistError

    def delete_user(self, user_uuid):
        if not self.does_user_exist(user_uuid):
            raise UserDoesNotExistError
        else:
            user = self.get_user_by_uuid(user_uuid)
            del self._graph[user]

    def follow(self, follower, followee):
        user_follows = self.get_user_by_uuid(follower)
        user_followed = self.get_user_by_uuid(followee)

        if user_followed not in self._graph.keys():
            raise UserDoesNotExistError
        if user_follows not in self._graph.keys():
            raise UserDoesNotExistError

        if user_followed in self._graph[user_follows]:
            pass
        else:
            self._graph[user_follows].append(user_followed)

    def unfollow(self, follower, followee):
        user_follows = self.get_user_by_uuid(follower)
        user_followed = self.get_user_by_uuid(followee)

        if user_followed not in self._graph.keys():
            raise UserDoesNotExistError
        if user_follows not in self._graph.keys():
            raise UserDoesNotExistError

        if user_followed in self._graph[user_follows]:
            self._graph[user_follows].remove(user_followed)
        else:
            pass

    def is_following(self, follower, followee):
        user_follows = self.get_user_by_uuid(follower)
        user_followed = self.get_user_by_uuid(followee)

        if user_followed not in self._graph.keys():
            raise UserDoesNotExistError
        if user_follows not in self._graph.keys():
            raise UserDoesNotExistError

        return user_followed in self._graph[user_follows]

    def followers(self, user_uuid):
        user_followed = self.get_user_by_uuid(user_uuid)
        if user_followed not in self._graph.keys():
            raise UserDoesNotExistError

        followers = []

        for key in self._graph.keys():
            if user_followed in self._graph[key]:
                followers.append(key)
        return set([f.uuid for f in followers])

    def following(self, user_uuid):
        user = self.get_user_by_uuid(user_uuid)
        if user not in self._graph.keys():
            raise UserDoesNotExistError
        return set([u.uuid for u in self._graph[user]])

    def friends(self, user_uuid):
        friends = set()
        user = self.get_user_by_uuid(user_uuid)
        if user not in self._graph.keys():
            raise UserDoesNotExistError
        for follower in self._graph[user]:
            if user in self._graph[follower]:
                friends.add(follower.get_uuid())
            else:
                pass
        return set(friends)

    def max_distance(self, user_uuid):
        user = self.get_user_by_uuid(user_uuid)
        if user not in self._graph.keys():
            raise UserDoesNotExistError
        all_paths = []
        if self._graph[user] == []:
            return 0
        else:
            for each in self._graph.keys():
                cur_path = self.min_dist_helper(user.uuid, each.uuid)
                if not cur_path == float('inf'):
                    all_paths.append(cur_path)
        return max(all_paths)

    def min_dist_helper(self, from_user_uuid, to_user_uuid):
        user_follows = self.get_user_by_uuid(from_user_uuid)
        user_followed = self.get_user_by_uuid(to_user_uuid)
        path = find_shortest_path(self._graph, user_follows, user_followed)
        return len(path) - 1

    def min_distance(self, from_user_uuid, to_user_uuid):
        user_follows = self.get_user_by_uuid(from_user_uuid)
        user_followed = self.get_user_by_uuid(to_user_uuid)
        if user_follows not in self._graph.keys():
            raise UserDoesNotExistError
        if user_followed not in self._graph.keys():
            raise UserDoesNotExistError
        distance = self.min_dist_helper(from_user_uuid, to_user_uuid)
        if distance == 0:
            raise UsersNotConnectedError
        else:
            return distance

    def nth_layer_followings(self, user_uuid, n):
        user = self.get_user_by_uuid(user_uuid)
        if user not in self._graph.keys():
            raise UserDoesNotExistError
        result = []
        all_users = self._graph.keys()
        tmp_d = {u: self.min_dist_helper(user_uuid, u.uuid) for u in all_users}
        for key, value in tmp_d.items():
            if value == n:
                result.append(key.uuid)
        return result

    def generate_feed(self, user_uuid, offset=0, limit=10):
        posts = []
        user = self.get_user_by_uuid(user_uuid)
        if user not in self._graph.keys():
            raise UserDoesNotExistError
        followees = self._graph[user]

        for followee in followees:
            tmp_queue = Queue(maxsize=MAX_SIZE_POST_QUEUE)
            while not followee.posts.empty():
                current_post = followee.posts.get()
                posts.append(current_post)
                tmp_queue.put(current_post)
            followee.posts = tmp_queue

        s_p = sorted(posts, key=lambda post: post.published_at, reverse=True)
        return s_p[offset:offset + limit]


class UserDoesNotExistError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class UsersNotConnectedError(Exception):
    pass


def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    shortest = []
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if shortest == [] or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest
