import urllib
import feedparser
import codecs

# Base api query url
base_url = 'http://export.arxiv.org/api/query?';

# Search parameters
search_query = 'au:Borodin_A OR Baik_J OR Corwin_I OR Gorin_V OR Petrov_L OR Barraquand_G OR Bufetov_A OR Kuan_J OR Rahman_M OR Shen_H OR Saenz_A OR Silva_G OR Sun_Y OR Tsai_L OR Knizel_A OR Sun_X OR Dimitrov_E OR Matetski_K OR Landon_B OR Korotkikh_S OR Peski_R OR Sitaraman_M OR Cuenca_C OR Aggarwal_A OR Ahn_A OR Liao_Y OR Wu_X OR Ghosal_P OR Parekh_S OR Rychnovsky_M OR Sitaraman_M OR Liu_Z OR Matveev_K OR Moll_A OR Lin_Y OR Russkikh_M'
start = 0
max_results = 100

query = 'search_query=%s&start=%i&max_results=%i&sortBy=submittedDate&sortOrder=descending' % (search_query,
                                                    start,
                                                    max_results)

# Opensearch metadata such as totalResults, startIndex, 
# and itemsPerPage live in the opensearch namespase.
# Some entry metadata lives in the arXiv namespace.
# This is a hack to expose both of these namespaces in
# feedparser v4.1
feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

# perform a GET request using the base_url and query
response = urllib.urlopen(base_url+query).read()

# parse the response using feedparser
feed = feedparser.parse(response)

# print out feed information
print 'Feed title: %s' % feed.feed.title
print 'Feed last updated: %s' % feed.feed.updated

# print opensearch metadata
print 'totalResults for this query: %s' % feed.feed.opensearch_totalresults
print 'itemsPerPage for this query: %s' % feed.feed.opensearch_itemsperpage
print 'startIndex for this query: %s'   % feed.feed.opensearch_startindex


# Run through each entry, and print out information
for entry in feed.entries:
    target_file = open (entry.published.split('T')[0] + '-' + entry.id.split('/abs/')[-1].split('v')[0] + '.md', 'w')

    target_file.write('---\n')
    target_file.write('layout: post\n')
    target_file.write('title: ' + entry.id.split('/abs/')[-1].split('v')[0] + ' [' + entry.tags[0]['term'] + ']\n')
    target_file.write('date: ' + entry.published + '\n')
    target_file.write('comments: false\n')
    target_file.write('tags: publication\n')
    target_file.write('published: true\n')
    target_file.write('---\n')
    target_file.write('\n')

    target_file.write('<b>' + '</b>, <b>'.join(author.name for author in entry.authors).encode('utf-8') + '</b>, "<i>')
    target_file.write(entry.title.encode('utf-8').replace('\n', '')  + '</i>" ([arXiv](')
    target_file.write(entry.id + '))\n')

    target_file.close()

