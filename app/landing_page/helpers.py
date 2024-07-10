from app.models import Member, Mitra, ActivityList

def get_achievements(request):
    try:
        # count total member
        total_member = Member.objects.all().count()
        # count total mitra
        total_mitra = Mitra.objects.all().count()
        # count total activity
        total_activity = ActivityList.objects.all().count()
        context = {
            'total_member': int(total_member),
            'total_mitra': int(total_mitra),
            'total_activity': int(total_activity),
        }
        return context
    except Exception as e:
        return 'Gagal mengambil data pencapaian: ' + str(e)
