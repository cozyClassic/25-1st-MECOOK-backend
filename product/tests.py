texts = 'SELECT `products`.`id`, `products`.`name`, `products`.`thumbnail_out_url`, `products`.`thumbnail_over_url`, `products`.`cook_time`, `products`.`servings_g_people`, `categories`.`name`, `products`.`priority` FROM `products` INNER JOIN `categories` ON (`products`.`category_id` = `categories`.`id`) WHERE `products`.`name` LIKE \'%\\"진한\\"%\''

print(texts.replace("`",""))
