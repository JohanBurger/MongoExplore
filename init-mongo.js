db = db.getSiblingDB('admin');
db.auth('root', 'super_secure_password');

db = db.getSiblingDB('explore-db');
db.createUser({
  user: 'app_user',
  pwd: 'app_user_password',
  roles: [
    {
      role: 'readWrite',
      db: 'explore-db',
    },
  ],
});

db.createCollection('test_docker');