alter table sys_user
    add user_photo varchar(256) null;

alter table article
    add like_num int default 0;

alter table comment
    add to_user varchar(8) null comment '回复者';

alter table comment
        add comment_status varchar(8) null comment '0 未读，1已读' default '0';


create table user_behavior
(
    id          int auto_increment
        primary key,
    user_code   varchar(256)                       null,
    phone_id    int                                null,
    create_time datetime default CURRENT_TIMESTAMP null,
    like_count  int                                null comment '点击次数'
)
    comment '用户行为';

