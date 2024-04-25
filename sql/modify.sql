alter table sys_user
    add user_photo varchar(256) null;

alter table article
    add like_num int default 0;

alter table comment
    add to_user varchar(8) null comment '回复者';

alter table comment
        add comment_status varchar(8) null comment '0 未读，1已读' default '0';

