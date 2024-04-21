create table article
(
    article_id      int auto_increment
        primary key,
    user            varchar(256) null,
    article_content longtext     null,
    article_picture varchar(256) null,
    article_time    datetime     null
)
    charset = utf8;

create index user
    on article (user);

create table comment
(
    comment_id      int auto_increment
        primary key,
    comment_content longtext     null,
    user            varchar(256) null,
    article_id      int          null,
    update_time     datetime     null
)
    charset = utf8;

create index article_id
    on comment (article_id);

create index user
    on comment (user);

create table mobile_company
(
    brand       varchar(256)  null,
    brand_score decimal(4, 1) null,
    brand_occup decimal(3, 1) null,
    good_score  decimal(4, 1) null,
    low_price   int           null,
    high_price  int           null,
    url         varchar(256)  null,
    update_time datetime      null
)
    charset = utf8;

create table mobile_detail
(
    cpu              varchar(256)  null,
    company_type     varchar(128)  null,
    id               int           not null
        primary key,
    type             varchar(256)  null,
    reference_price  decimal(6, 1) null,
    param_url        varchar(256)  null,
    market_date      varchar(256)  null,
    resolution       varchar(256)  null,
    screen_size      varchar(256)  null,
    internal_storage varchar(256)  null,
    font_camera      varchar(256)  null,
    rear_camera      varchar(256)  null,
    kernel_count     varchar(256)  null,
    battery_capacity varchar(256)  null,
    battery_type     varchar(256)  null,
    cost_performance double        null,
    performance      double        null,
    continuation     double        null,
    appearance       double        null,
    photograph       double        null,
    four_five_star   varchar(5)    null,
    three_four_star  varchar(5)    null,
    two_three_star   varchar(5)    null,
    one_two_star     varchar(5)    null,
    score            double        null,
    descript         varchar(1024) null,
    evaluate_url     varchar(128)  null,
    detail_descript  varchar(1024) null,
    url              varchar(128)  null,
    update_time      datetime      null,
    review_count     int default 0 null,
    img_url          varchar(1024) null
)
    charset = utf8;

create table sys_user
(
    user_code varchar(256) not null
        primary key,
    pswd      varchar(256) null,
    e_mail    varchar(256) null,
    stu_id    varchar(256) null,
    question  varchar(256) null,
    answer    varchar(256) null,
    dates     datetime     null
)
    charset = utf8;

