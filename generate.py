from tweepy import *
import sys

if len(sys.argv) != 7:
    print('%s <consumer_key> <consumer_secret> <oauth_token> <oauth_token_secret> <owner_screen_name> <list_name>' % sys.argv[0])
    sys.exit(1)


consumer_key = sys.argv[1]
consumer_secret = sys.argv[2]
oauth_token = sys.argv[3]
oauth_token_secret = sys.argv[4]
owner_screen_name = sys.argv[5]
list_name = sys.argv[6]

logstash_conf_input = '''input { 
    twitter {
        consumer_key => "%s"
        consumer_secret => "%s"
        oauth_token => "%s"
        oauth_token_secret => "%s"
        follows => ["%s"]
        type => stream
        add_field => {"list" => "%s"}
        # owner screen name (%s)
    }
} 
'''
logstash_conf_filter = '''filter {
    if [type] == "stream" {

        if ([hashtags]) {
            ruby {
                code => '    
                i = 0
                event.get("[hashtags]").each {|hash|
                    if event.get("hashtags_text")
                        event.set("[hashtags_text]", event.get("hashtags_text") + [event.get("[hashtags][#{i}][text]").downcase])
                    else
                        event.set("[hashtags_text]", [event.get("[hashtags][#{i}][text]").downcase])
                    end
                    i += 1
                }'
            }
        }
        mutate{
            remove_field => ["doc", hashtags]
        }
        mutate{
            rename => { "hashtags_text" => "hashtags" }
        }
    }
}'''

logstash_conf_output = '''
output {
    if [type] == "stream" {
        elasticsearch {
            hosts => ["127.0.0.1:9200"]
            index => "twitter-%{+YYYY-MM}"
            document_type => "stream"
        }
    }
}
'''

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(oauth_token, oauth_token_secret)
api = API(auth)
follower_ids = []
for member in Cursor(api.list_members,slug=list_name, owner_screen_name=owner_screen_name).items():
    follower_ids.append(member.id_str)

print(logstash_conf_input % (consumer_key, consumer_secret, oauth_token, oauth_token_secret, '","'.join(follower_ids), list_name, owner_screen_name))
print(logstash_conf_filter)
print(logstash_conf_output)
