BEGIN;
--
-- Create model Post
--
CREATE TABLE "blog_post" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
 "title" varchar(264) NOT NULL,
  "slug" varchar(264) NOT NULL, 
  "body" text NOT NULL,
  "published" datetime NOT NULL, 
  "created" datetime NOT NULL,
   "updated" datetime NOT NULL,
    "status" varchar(16) NOT NULL,
     "author_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "blog_post_slug_b95473f2" ON "blog_post" ("slug");
CREATE INDEX "blog_post_author_id_dd7a8485" ON "blog_post" ("author_id");
COMMIT;
